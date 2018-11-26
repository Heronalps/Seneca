# This function samples the compute charge of lambda under different allocated memory

import botocore, boto3, botocore, json, base64, re, math
config = botocore.config.Config(connect_timeout=300, read_timeout=300)
client = boto3.client("lambda", config=config)

fn_name = "random_num_workload"
aws_role = "arn:aws:iam::603495292017:role/lambda"
payload = json.dumps({ "number": "50"})

def invoke(fn_name, payload):
    response = client.invoke(
        FunctionName = fn_name,
        InvocationType = 'RequestResponse',
        LogType = 'Tail',
        Payload = payload
    )
    # print(response)
    request_id = response['ResponseMetadata']['RequestId']
    log_string = base64.b64decode(response['LogResult']).decode('utf-8')
    # print(log_string)
    billed_duration = int(re.search(r'(?<=\tBilled\sDuration:\s)(.*?)(?=\sms)', log_string).group(0))
    memory_size = int(re.search(r'(?<=\tMemory\sSize:\s)(.*?)(?=\sMB)', log_string).group(0))
    max_memory_used = int(re.search(r'(?<=\tMax\sMemory\sUsed:\s)(.*?)(?=\sMB)', log_string).group(0))
    compute_charge = billed_duration * 1e-3 * memory_size / 1024 # unit Gb-Sec

    metrics = {
        "billed_duration" : billed_duration,
        "max_memory_used" : max_memory_used,
        "memory_size" : memory_size,
        "compute_charge" : compute_charge
    }

    return metrics
 
def update_config(fn_name, memory_size):
    print("update allocated memory to {0} MB".format(memory_size))
    response = client.update_function_configuration(
        FunctionName = fn_name,
        MemorySize = memory_size
    )

def sampling(num):
    path = "./sampling{0}.data".format(num)
    
    for i in range(4, 48):
        update_config(fn_name, i * 64)
        metrics = invoke(fn_name, payload)
        with open(path, 'a+') as f:
            f.write(json.dumps(metrics) + '\n')

if __name__ == "__main__":
    sampling(2)