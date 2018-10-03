import json, boto3, time, re

def lambda_handler(event, context):
    client = boto3.client('logs')
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    metrics_table = dynamodb.Table('container_test_metrics')
    response_table = dynamodb.Table('container_test_response')
    requestId_identifier_hash = {}
    
    response = client.describe_log_streams(
        logGroupName = '/aws/lambda/container_tester',
        orderBy = 'LastEventTime',
        descending = True
    )
    for stream_name in response['logStreams']:
        # print(stream_name['logStreamName'])
        logs = client.get_log_events(
            logGroupName='/aws/lambda/container_tester',
            logStreamName= stream_name['logStreamName']
        )
        print("===Log==")
        print(logs)   
        print("=====")
    
        for event in logs['events']:
            message = event['message']
                
            if message.startswith('REPORT'):
                requestId = re.search(r'(?<=RequestId:\s)(.*?)(?=\t)', message)
                identifier = requestId_identifier_hash[requestId.group(0)]
                
                # Milliseconds
                duration = re.search(r'(?<=\tDuration:\s)(.*?)(?=\sms)', message)
                billed_duration = re.search(r'(?<=\tBilled\sDuration:\s)(.*?)(?=\sms)', message)
        
                # Megabytes
                memory_size = re.search(r'(?<=\tMemory\sSize:\s)(.*?)(?=\sMB)', message)
                max_memory_used = re.search(r'(?<=\tMax\sMemory\sUsed:\s)(.*?)(?=\sMB)', message)
    
                metrics_table.put_item(
                    Item = {
                        'identifier': identifier,
                        'duration': duration.group(0),
                        'billed_duration': billed_duration.group(0),
                        'memory_size': memory_size.group(0),
                        'max_memory_used':max_memory_used.group(0)
                    }
                )
            elif message.startswith('{'):
                identifier = re.search(r'(?<=\'identifier\':\s\')(.*?)(?=\')', message)
                requestId = re.search(r'(?<=\'requestId\':\s\')(.*?)(?=\')', message)
                result = re.search(r'(?<=\'Message\':\s\')(.*?)(?=\')', message)
                
                requestId_identifier_hash[requestId.group(0)] = identifier.group(0)
                # print(requestId_identifier_hash)
                response_table.put_item(
                    Item = {
                        'identifier': identifier.group(0),
                        'response': result.group(0)
                    }
                )