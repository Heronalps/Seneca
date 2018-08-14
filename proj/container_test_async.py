import time, os, sys, boto3, json, decimal
from datetime import datetime

containerId = str(int(time.time()))[-6:]
configTimestamp = str(datetime.now())
local_repo = os.path.join(os.path.sep, "tmp", os.path.basename('container'))

def lambda_handler(event, context):
    response = ''
    if event['messageType'] == 'work':
        response = "Container " + containerId + ": work is done with timestamp " + configTimestamp

    elif event['messageType'] == 'refreshConfig':
        configTimestamp2 = str(datetime.now())
        response = "Container " + containerId + ": work is done with timestamp " + configTimestamp2
    
    elif event['messageType'] == 'writeId':
        if not os.path.exists(local_repo):
            os.makedirs(local_repo)

        with open(local_repo + "Id.txt", 'w') as f:
            f.write(containerId)
        response = "Successfully write container id " + containerId + " to " + local_repo + "Id.txt"

    elif event['messageType'] == 'retrieveId':
        try:
            with open(local_repo + 'Id.txt') as f:
                container_id = f.read()
        except FileNotFoundError:
            response = "The container id is not saved in this lambda " + containerId + " container."
        if not response:
            response =  "Retrieved Container id : " + container_id

    if event['invokeType'] == 'Event':
        writeToDynamoDB(response)
    elif event['invokeType'] == 'RequestResponse':
        return response

def writeToDynamoDB(response):
    time_stamp = int(time.time())
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('container_test_table')
    response = table.put_item(
       Item = {
            'timeStamp': time_stamp,
            'response': response
        }
    )