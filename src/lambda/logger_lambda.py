import json, boto3, time, re

client = boto3.client('logs')
s3 = boto3.resource('s3', region_name='us-west-2')
metrics_bucket = 'container-test-metrics'
response_bucket = 'container-test-response'

def write_to_s3(bucket, key, data, metadata):
    s3.Bucket(bucket).put_object(Key=key, Body=data, Metadata=metadata)

def lambda_handler(event, context):
    requestId_identifier_hash = {}
    
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
        print("===Log==")
        print(logs)   
        print("=====")
    
        for event in logs['events']:
            message = event['message']
                
            if message.startswith('{'):
                identifier = re.search(r'(?<=\'identifier\':\s\')(.*?)(?=\')', message).group(0)
                requestId = re.search(r'(?<=\'requestId\':\s\')(.*?)(?=\')', message).group(0)
                result = re.search(r'(?<=\'Message\':\s\')(.*?)(?=\')', message).group(0)
                
                requestId_identifier_hash[requestId] = identifier

                write_to_s3(response_bucket, identifier, result, {})

            elif message.startswith('REPORT'):
                requestId = re.search(r'(?<=RequestId:\s)(.*?)(?=\t)', message).group(0)
                identifier = requestId_identifier_hash[requestId]
                
                # Milliseconds
                duration = re.search(r'(?<=\tDuration:\s)(.*?)(?=\sms)', message).group(0)
                billed_duration = re.search(r'(?<=\tBilled\sDuration:\s)(.*?)(?=\sms)', message).group(0)
        
                # Megabytes
                memory_size = re.search(r'(?<=\tMemory\sSize:\s)(.*?)(?=\sMB)', message).group(0)
                max_memory_used = re.search(r'(?<=\tMax\sMemory\sUsed:\s)(.*?)(?=\sMB)', message).group(0)

                metrics = json.dumps({
                    'duration': duration,
                    'billed_duration': billed_duration,
                    'memory_size': memory_size,
                    'max_memory_used':max_memory_used
                })
                write_to_s3(metrics_bucket, identifier, metrics, {})