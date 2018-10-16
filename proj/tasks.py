from .celery import app
import json, boto3, time

@app.task
def add(x, y):
    return x + y

@app.task
def mul(x, y):
    return x * y

@app.task
def xsum(numbers):
    return sum(numbers)

@app.task
def invoke_sync():
    session = boto3.Session(profile_name='default')
    client = session.client('lambda')

    response = client.invoke(
        FunctionName='container_tester',
        InvocationType='RequestResponse',
        LogType='None',
        Payload=json.dumps({ "messageType" : "refreshConfig", "invokeType" : "RequestResponse" })
    )
    res_json = json.loads(response['Payload'].read().decode("utf-8"))
    response['Payload'] = res_json
    return response

@app.task
def invoke_async():
    session = boto3.Session(profile_name='default')
    client = session.client('lambda')

    response = client.invoke(
        FunctionName='container_tester',
        InvocationType='Event',
        LogType='None',
        Payload=json.dumps({ "messageType" : "refreshConfig", "invokeType" : "Event" })
    )

    return "Response Status Code : " + str(response['StatusCode'])

@app.task
def invoke_centaurus_worker(payload):
    session = boto3.Session(profile_name='default')
    client = session.client('lambda')

    response = client.invoke(
        FunctionName = 'create_job',
        InvocationType = "RequestResponse",
        LogType = 'None',
        Payload = payload
    )
    return response