import time, os, sys, boto3, json, decimal
from datetime import datetime
from dependencies import build_response

containerId = str(int(time.time()))[-6:]
configTimestamp = str(datetime.now())
local_repo = os.path.join(os.path.sep, "tmp", os.path.basename('container'))

def lambda_handler(event, context):
    response = build_response(event)
    response['requestId'] = context.aws_request_id
    
    # Generate Log events
    print(response)
    return response