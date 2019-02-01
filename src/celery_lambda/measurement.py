import json, time, boto3, re, sys, os
from datetime import datetime
from src.celery_lambda.clean_logs import clean_logs

# Measurement module
#
# This module is a measurement tool for batch lambda invocation.
# It is written in a way of decoupling measurement from lambda source code.
#
# Ideally, this tool should only take lambda name and measure metrics 
# without any requirement from lambda source code.
#
# Calling chain: show_result (Entrance of Measurement)
#                    |
#                    -> retrieve_result -> parse_log 


# show_result() 
# This function retrieve execution result from log retriever, print them to stdout 
# and persist them to local file sytem.

def show_result(lambda_name, celery_async, lambda_async, host_execu_time):

    # TODO - I keep celery_async and lambda_async for experiments now. 
    # I will come up with a better naming for data files in storage
    # in order to root out these two parameters.

    group_response, metrics = retrieve_result(lambda_name)
    invoke_time = metrics["invoke_time"]
    # Print returned values from retrieve_result
    metrics["host_execu_time"] = host_execu_time

    print("===============================Responses=============================")
    for response in group_response:
        print (response)
    
    print("===============================Metrics===============================")
    print("Host Execution Time : %.4f milliseconds" %metrics['host_execu_time'])
    print("Total Time Spent on Lambda : %.4f milliseconds" %metrics['total_duration'])
    print("Invocation Times : %d times" %invoke_time)
    print("Time Spent per Invocation : %.4f milliseconds" %metrics['duration_per_invocation'])
    print("Total Billed Duration : %.4f milliseconds" %metrics['total_billed_duration'])
    print("Max Memory Used : %d MBs" %metrics['max_memory_used'])
    print("Memory Allocated : %d MBs" %metrics['memory_size'])
    print("Total Compute Charge : %.4f GB-seconds" %metrics['compute_charge'])
    print("Total Cost : $ %f "%metrics['cost'])
    print("====================================================================")

    # Generate file name with timestamp
    # timestamp = datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
    timestamp = datetime.fromtimestamp(time.time()).strftime('%Y%m%d')
    celery_label = "CA" if celery_async else "CS"
    lambda_label = "LA" if lambda_async else "LS"
    
    # response_path = "./result/response_" + celery_label + str(invoke_time) + lambda_label + "_" + timestamp + ".data"
    # response_json_str = json.dumps(group_response)
    # with open(response_path, 'a+') as f:
    #     f.write(response_json_str + '\n')
    
    metrics_path = "./result/metrics_" + celery_label + str(invoke_time) + lambda_label + "_" + timestamp + ".data"
    metrics_json_str = json.dumps(metrics)
    with open(metrics_path, 'a+') as f:
        f.write(metrics_json_str + '\n')

    return metrics_path #, response_path

# retrieve_result()
# This function will retrieve result from parse_log and calculate metrics for batch invocation
# All pricing model calculation should come to here.

def retrieve_result(lambda_name):
    total_duration = 0
    total_billed_duration = 0
    max_memory_used = 0
    memory_size = 0
    group_response, group_metrics = parse_log(lambda_name)
    invoke_time = len(group_metrics)

    for metrics in group_metrics:
        total_duration += float(metrics['duration'])
        total_billed_duration += float(metrics['billed_duration'])
        temp = int(metrics['max_memory_used'])
        if temp > max_memory_used:
            max_memory_used = temp
        memory_size = int(metrics['memory_size'])
    
    duration_per_invocation = total_duration / invoke_time
    compute_charge = total_billed_duration * 0.001 * (memory_size / 1024)
    
    # cost = compute charge + request charge
    cost = 0.00001667 * compute_charge

    # Other metrics can be calculated here:
    # Total / Average / Stdev of 
    # 

    metrics = {
        "total_duration" : total_duration, 
        "total_billed_duration" : total_billed_duration,
        "max_memory_used" : max_memory_used, 
        "memory_size" : memory_size, 
        "duration_per_invocation" : duration_per_invocation, 
        "compute_charge" : compute_charge,
        "cost" : cost,
        "invoke_time" : invoke_time
    }

    return group_response, metrics

# parse_log()
# This function parses cloudwatch log to extract four metrics of lambda invocation

def parse_log(log_group_name):
    # Wait for last batch of log written into cloudwatch
    time.sleep(10)
    group_response = []
    group_metrics = []
    log_client = boto3.client('logs')
    messages = []

    response = log_client.describe_log_streams(
        logGroupName = log_group_name,
        orderBy = 'LastEventTime',
        descending = True
    )
    for stream_name in response['logStreams']:
        logs = log_client.get_log_events(
            logGroupName = log_group_name,
            logStreamName = stream_name['logStreamName']
        )
        # print("===Log==")
        # print(logs)   
        # print("=====")
    
        for event in logs['events']:
            message = event['message']
            
            messages.append(message)
            
            if message.startswith('REPORT'):
                
                # Milliseconds
                duration = re.search(r'(?<=\tDuration:\s)(.*?)(?=\sms)', message).group(0)
                billed_duration = re.search(r'(?<=\tBilled\sDuration:\s)(.*?)(?=\sms)', message).group(0)
        
                # Megabytes
                memory_size = re.search(r'(?<=\tMemory\sSize:\s)(.*?)(?=\sMB)', message).group(0)
                max_memory_used = re.search(r'(?<=\tMax\sMemory\sUsed:\s)(.*?)(?=\sMB)', message).group(0)

                metrics = {
                    'duration': duration,
                    'billed_duration': billed_duration,
                    'memory_size': memory_size,
                    'max_memory_used':max_memory_used
                }
                group_metrics.append(metrics)
            
            elif not message.startswith('START') and not message.startswith('END'):
                temp_result = re.search(r'(?<=\'Message\':\s\')(.*?)(?=\')', message)
                if temp_result:
                    result = temp_result.group(0)
                    group_response.append(result)
    ts = round(time.time())

    with open("./cloudwatch/log_" + str(ts) + ".data", "w") as f:
        for m in messages:
            f.write("%s\n" % m)

    return group_response, group_metrics