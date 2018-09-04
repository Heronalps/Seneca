import time, os, sys, boto3, json, decimal, uuid
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr

containerId = str(int(time.time()))[-6:]
configTimestamp = str(datetime.now())
local_repo = os.path.join(os.path.sep, "tmp", os.path.basename('container'))

def lambda_handler(event, context):
    response = ''
    timestamp = time.time()
    if event['messageType'] == 'work':
        response = {
            'Message' : "Container " + containerId + ": work is done with timestamp " + configTimestamp,
            'Timestamp' : timestamp
        }

    elif event['messageType'] == 'refreshConfig':
        configTimestamp2 = str(datetime.now())
        response = {
            'Message' : "Container " + containerId + ": work is done with timestamp " + configTimestamp2,
            'Timestamp' : timestamp
        }
    
    elif event['messageType'] == 'writeId':
        if not os.path.exists(local_repo):
            os.makedirs(local_repo)

        with open(local_repo + "Id.txt", 'w') as f:
            f.write(containerId)
        response = {
            'Message' : "Successfully write container id " + containerId + " to " + local_repo + "Id.txt",
            'Timestamp' : timestamp
            }

    elif event['messageType'] == 'retrieveId':
        try:
            with open(local_repo + 'Id.txt') as f:
                container_id = f.read()
        except FileNotFoundError:
            response = {
                'Message' : "The container id is not saved in this lambda " + containerId + " container.",
                'Timestamp' : timestamp
            }
        if not response:
            response =  {
                'Message' : "Retrieved Container id : " + container_id,
                'Timestamp' : timestamp
            }

    if event['invokeType'] == 'Event':
        writeToDynamoDB(json.dumps(response), event['uuid'])
    elif event['invokeType'] == 'RequestResponse':
        return json.dumps(response)

def writeToDynamoDB(response, uuid):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('container_test_table')
    response = table.put_item(
       Item = {
            'identifier': uuid,
            'response': response
        }
    )