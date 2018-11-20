import boto3, botocore, json, base64, re, math

client = boto3.client("lambda")

fn_name = "container_test_lambda"
aws_role = "arn:aws:iam::603495292017:role/lambda"
payload = json.dumps({ "messageType" : "refreshConfig", "invokeType" : "RequestResponse" })

def create_function(fn_name, aws_role):
    functions = client.list_functions()['Functions']
    created = False
    for func in functions:
        if func['FunctionName'] == fn_name:
            created = True
            print("Function {0} has been created!".format(fn_name))
    
    if not created:
        print("Function has not been created yet!")
        response = client.create_function(
            FunctionName= fn_name,
            Runtime= "python3.6",
            Role= aws_role,
            Handler= "{0}.lambda_handler".format(fn_name),
            Code={ 'ZipFile' : open("{0}.zip".format(fn_name), 'rb').read()},
            # Set default memory as maximum allocated memory
            MemorySize= 3008
        )
        # print(response)

def invoke(fn_name, payload):
    # Warm up the lambda container
    client.invoke(
        FunctionName = fn_name,
        InvocationType = 'RequestResponse',
        LogType = 'Tail',
        Payload = payload
    )
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

    return billed_duration, memory_size, max_memory_used

def update_config(fn_name, memory_size):
    print("update allocated memory to {0} MB".format(memory_size))
    response = client.update_function_configuration(
        FunctionName = fn_name,
        MemorySize = memory_size
    )

def compute():
    billed_duration, memory_size, max_memory_used = invoke(fn_name, payload)
    compute_charge = billed_duration * 1e-3 * memory_size / 1024
    print("The compute charge is {0} GB-Sec".format(compute_charge))
    return compute_charge, max_memory_used

def optimize():
    create_function(fn_name, aws_role)
    # Baseline of compute charge and allocated memory
    compute_charge, max_memory_used = compute()
    # Binary search for optimized allocated memory
    if max_memory_used <= 128:
        start = 2
    else:
        end = math.ceil(max_memory_used / 64)

    end = round(3008 / 64)

    while (start < end):
        mid = math.floor((start + end) / 2)
        update_config(fn_name, mid * 64)
        temp, _ = compute()

        if mid == 0:
            left = temp
        else:
            update_config(fn_name, (mid - 1) * 64)
            left, _ = compute()
        
        if mid == round(3008 / 64):
            right = temp
        else:
            update_config(fn_name, (mid + 1) * 64)
            right, _ = compute()

        if (left < right):
            end = mid - 1
        else:
            start = mid + 1
    
    update_config(fn_name, start * 64)
    print("The optimized allocated memory is {0}MB".format(start * 64))

if __name__ == "__main__":
    optimize()