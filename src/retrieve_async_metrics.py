import json, re, boto3, time

def lambda_handler(event, context):
    
    print("===event====")
    print(event)
    records = event['Records']
    
    for record in records:
        if record['eventName'] != 'INSERT':
            return
        
        response = record['dynamodb']['NewImage']['response']['S']
        requestId = re.search(r'(?<="requestId":\s")(.*?)(?=")', response).group(0)
        # print("===Record===")
        # print(record)
        # print("===requestId===")
        # print(requestId)
        
        
        identifier = re.search(r'(?<="identifier":\s")(.*?)(?=")', response).group(0)
        # print("====identifier===")
        # print(identifier)
        
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        sync_metrics = dynamodb.Table('container_test_metrics')
        async_metrics = dynamodb.Table('container_test_async_metrics')
        
        # Wait metrics to be written
        time.sleep(2)
        
        response = sync_metrics.get_item(
          Key = {
                'requestId': requestId
            }
        )
        # print("====response====")
        # print(response)
        item = response['Item']
        
        async_metrics.put_item(
            Item = {
                'identifier': identifier,
                'duration': item['duration'],
                'billed_duration': item['billed_duration'],
                'memory_size': item['memory_size'],
                'max_memory_used': item['max_memory_used']
            }    
        )
