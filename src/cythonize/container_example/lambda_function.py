from datetime import datetime
from dependencies import build_response


def lambda_handler(event, context):
    response = build_response(event)
    response['requestId'] = context.aws_request_id
    
    # Generate Log events
    print(response)
    return response