from .celery import app
import json, boto3, time
from botocore.client import Config

@app.task
def add(x, y):
    return x + y

@app.task
def mul(x, y):
    return x * y

@app.task
def xsum(numbers):
    return sum(numbers)
'''
This function invokes lambda with specific payload

Parameters:
    fucntion_name : string
    sync : boolean
    payload: A Python map object (Not json serialized)
    decoder : string
Return:
    response
'''
@app.task
def invoke_lambda(function_name, sync=True, payload={}, decoder='utf-8'):
    session = boto3.Session(profile_name='default')
    config = Config(connect_timeout=900, read_timeout=900)
    client = session.client('lambda', config=config)
    invocation_type = 'RequestResponse' if sync else 'Event'
    response = client.invoke(
        FunctionName=function_name,
        InvocationType=invocation_type,
        LogType='None',
        Payload=json.dumps(payload)
    )
    if sync:
        res_json = json.loads(response['Payload'].read().decode(decoder))
        response['Payload'] = res_json
        return response
    else:
        return "Response Status Code : " + str(response['StatusCode'])
