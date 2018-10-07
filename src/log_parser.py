import json, boto3, time, re

client = boto3.client('logs')

def parse_log(log_group_name):
    _requestId_identifier_hash = {}
    group_response = []
    group_metrics = []
    
    response = client.describe_log_streams(
        logGroupName = '/aws/lambda/container_tester',
        orderBy = 'LastEventTime',
        descending = True
    )
    for stream_name in response['logStreams']:
        logs = client.get_log_events(
            logGroupName='/aws/lambda/container_tester',
            logStreamName= stream_name['logStreamName']
        )
        # print("===Log==")
        # print(logs)   
        # print("=====")
    
        for event in logs['events']:
            message = event['message']
                
            if message.startswith('{'):
                _identifier = re.search(r'(?<=\'identifier\':\s\')(.*?)(?=\')', message).group(0)
                _requestId = re.search(r'(?<=\'requestId\':\s\')(.*?)(?=\')', message).group(0)
                result = re.search(r'(?<=\'Message\':\s\')(.*?)(?=\')', message).group(0)
                
                #requestId_identifier_hash[requestId] = identifier
                group_response.append(result)

            elif message.startswith('REPORT'):
                _requestId = re.search(r'(?<=RequestId:\s)(.*?)(?=\t)', message).group(0)
                
                # Because the REPORT cloudwatch event is not necessarily after Message event,
                # requestId and identifier mapping doesn't always work. So to root out mapping.

                # identifier = requestId_identifier_hash[requestId]
                
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
    
    return group_response, group_metrics