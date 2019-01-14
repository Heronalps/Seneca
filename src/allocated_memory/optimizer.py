import boto3, botocore, json, base64, re, math, collections

Config = botocore.config.Config(connect_timeout=900, read_timeout=900)
client = boto3.client("lambda", config=Config)

# client.meta.events._unique_id_handlers['retry-config-lambda']['handler']._checker.__dict__['_max_attempts'] = 0

fn_name = "random_num_workload"
# fn_name = "container_test_lambda"
aws_role = "arn:aws:iam::603495292017:role/lambda"
# The max length of queue used for monotonically increase decision
queue_max_len = 5
slope_increase = 1

# This input could possibly impact the outocome of optimization, 
# meaning the varying parameter could lead to different sweetspot in the real-world execution.
payload = json.dumps({ "number" : "50" })
# payload = json.dumps({
#   "messageType": "refreshConfig",
#   "invokeType": "RequestResponse"
# })

def create_function(fn_name, aws_role):
    functions = client.list_functions()['Functions']
    created = False
    for func in functions:
        if func['FunctionName'] == fn_name:
            created = True
            update_config(fn_name, 3008)
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
    
    request_id = response['ResponseMetadata']['RequestId']
    log_string = base64.b64decode(response['LogResult']).decode('utf-8')
    billed_duration = int(re.search(r'(?<=\tBilled\sDuration:\s)(.*?)(?=\sms)', log_string).group(0))
    memory_size = int(re.search(r'(?<=\tMemory\sSize:\s)(.*?)(?=\sMB)', log_string).group(0))
    max_memory_used = int(re.search(r'(?<=\tMax\sMemory\sUsed:\s)(.*?)(?=\sMB)', log_string).group(0))
    
    # The flag of the lower bound of lambda function
    process_exit = True if re.search(r'Process exited before completing request', log_string) else False
    compute_charge = billed_duration * 1e-3 * memory_size / 1024
    print("======")
    print (log_string)
    print("======")
    print(compute_charge)
    print("======")
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
    metrics = invoke(fn_name, payload)
    starting_point = math.ceil(metrics['max_memory_used'] / 64)
    if starting_point == 1: 
        starting_point = starting_point + 1
    minimum_compute_charge = 0.0
    allocated_memory = 0
    prev_memory = collections.deque(maxlen = queue_max_len)
    prev_compute_charge = collections.deque(maxlen = queue_max_len)
    optimization_cost = 0.0

    # Search from starting point of lower bound to sweet spot
    for num in range (starting_point, 47, 1): 
        update_config(fn_name, num * 64)
        metrics = invoke(fn_name, payload)
        optimization_cost = optimization_cost + metrics['compute_charge'] * 0.00001667
        if metrics['process_exit']:
            continue
        prev_compute_charge.append(metrics['compute_charge'])
        prev_memory.append(num * 64)

        if (isSweetspot(prev_compute_charge)):
            allocated_memory = prev_memory.popleft()
            break

    update_config(fn_name, allocated_memory)
    print ("The lambda function has been configured at {0} MB as allocated memory!".format(allocated_memory))
    print ("The cost of optimizing lambda function is ${0} !".format(optimization_cost))

# Ideally, the user should specify a lambda deployment package and this script
# will optimize the function configuration for you.

def isSweetspot(time_series):
    if time_series.maxlen != len(time_series):
        return False
    
    flag = True
    prev = 0.0
    for ts in time_series:
        if ts <= prev:
            flag = False
        else:
            prev = ts
    slope = (time_series[-1] - time_series[0]) / time_series.maxlen
    if slope < slope_increase:
        flag = False
    return flag

if __name__ == "__main__":
    optimize()
    # print(isSweetspot([1.0, 2.0, 3.0, 4.0, 3.9]))