import time, os, sys, boto3, json, decimal, uuid
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr

containerId = str(int(time.time()))[-6:]
configTimestamp = str(datetime.now())
local_repo = os.path.join(os.path.sep, "tmp", os.path.basename('container'))

def lambda_handler(event, context):
    for record in event['Records']:
        response = ''
        body = json.loads(record['body'])
        if body['messageType'] == 'work':
            response = {
                'Message' : "Container " + containerId + ": work is done with timestamp " + configTimestamp
            }
    
        elif body['messageType'] == 'refreshConfig':
            configTimestamp2 = str(datetime.now())
            response = {
                'Message' : "Container " + containerId + ": work is done with timestamp " + configTimestamp2
            }
        
        elif body['messageType'] == 'writeId':
            if not os.path.exists(local_repo):
                os.makedirs(local_repo)
    
            with open(local_repo + "Id.txt", 'w') as f:
                f.write(containerId)
            response = {
                'Message' : "Successfully write container id " + containerId + " to " + local_repo + "Id.txt"
            }
    
        elif body['messageType'] == 'retrieveId':
            try:
                with open(local_repo + 'Id.txt') as f:
                    container_id = f.read()
            except FileNotFoundError:
                response = {
                    'Message' : "The container id is not saved in this lambda " + containerId + " container."
                }
            if not response:
                response =  {
                    'Message' : "Retrieved Container id : " + container_id
                }
                
        response['identifier'] = body['uuid']
        response['requestId'] = context.aws_request_id
        
        # Generate Log events
        print(response)
        # return response