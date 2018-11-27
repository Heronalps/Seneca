import boto3, botocore, json, base64, re, math

Config = botocore.config.Config(connect_timeout=300, read_timeout=300)
client = boto3.client("lambda", config=Config)

client.meta.events._unique_id_handlers['retry-config-lambda']['handler']._checker.__dict__['_max_attempts'] = 0

fn_name = "random_num_workload"
aws_role = "arn:aws:iam::603495292017:role/lambda"
payload = json.dumps({ "number" : "50" })

def create_function(fn_name, aws_role):
    functions = client.list_functions()['Functions']
    created = False
    for func in functions:
        if func['FunctionName'] == fn_name:
            created = True
            print("Function {0} has been created!".format(fn_name))
    
    if not created:
        print("Function has not been created yet!")
        client.create_function(
            FunctionName= fn_name,
            Runtime= "python3.6",
            Role= aws_role,
            Handler= "{0}.lambda_handler".format(fn_name),
            Code={ 'ZipFile' : open("{0}.zip".format(fn_name), 'rb').read()},
            
            # Set default allocated memory as much as possible 
            MemorySize= 3008
        )
        # print(response)

def invoke(fn_name, payload):
    # Warm up the lambda container
    # client.invoke(
    #     FunctionName = fn_name,
    #     InvocationType = 'RequestResponse',
    #     LogType = 'Tail',
    #     Payload = payload
    # )
    response = client.invoke(
        FunctionName = fn_name,
        InvocationType = 'RequestResponse',
        LogType = 'Tail',
        Payload = payload
    )
    print (response)
    request_id = response['ResponseMetadata']['RequestId']
    log_string = base64.b64decode(response['LogResult']).decode('utf-8')
    billed_duration = int(re.search(r'(?<=\tBilled\sDuration:\s)(.*?)(?=\sms)', log_string).group(0))
    memory_size = int(re.search(r'(?<=\tMemory\sSize:\s)(.*?)(?=\sMB)', log_string).group(0))
    max_memory_used = int(re.search(r'(?<=\tMax\sMemory\sUsed:\s)(.*?)(?=\sMB)', log_string).group(0))
    
    # The flag of the lower bound of lambda function
    process_exit = True if re.search(r'Process exited before completing request', log_string) else False
    compute_charge = billed_duration * 1e-3 * memory_size / 1024
    
    metrics = {
        "billed_duration" : billed_duration,
        "max_memory_used" : max_memory_used,
        "memory_size" : memory_size,
        "compute_charge" : compute_charge,
        "process_exit" : process_exit
    }
    return metrics

def update_config(fn_name, memory_size):
    print("update allocated memory to {0} MB".format(memory_size))
    response = client.update_function_configuration(
        FunctionName = fn_name,
        MemorySize = memory_size
    )

# This function optimizes the allocated memory of Lambda by linear search
# due to the fluctuation of the compute charge. It literally tries out 
# allocated memory from the upper bound (3008 MB) to lower bound able to 
# execute lambda function.

def optimize():
    create_function(fn_name, aws_role)
    minimum_compute_charge = float("inf")
    allocatted_memory = math.inf
    
    # Search from upper bound to lower bound
    for num in range(47, 1, -1):
        update_config(fn_name, num * 64)
        metrics = invoke(fn_name, payload)
        if metrics['process_exit']:
            break
        # If two allocated memory generate same compute charge, the higher wins for lower duration
        
        if metrics['compute_charge'] < minimum_compute_charge:
            minimum_compute_charge = metrics['compute_charge']
            allocatted_memory = num * 64
    
    update_config(fn_name, allocatted_memory)
    print ("The lambda function has been configured at {0} MB as allocated memory!".format(allocatted_memory))

# Ideally, the user should specify a lambda deployment package and this script
# will optimize the function configuration for you.

if __name__ == "__main__":
    optimize()