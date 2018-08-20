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
def invoke_sync(param):
    session = boto3.Session(profile_name='racelab')
    client = session.client('lambda')

    response = client.invoke(
        FunctionName='container_tester',
        InvocationType='RequestResponse',
        LogType='None',
        Payload=json.dumps({ "messageType" : "work", "invokeType" : "RequestResponse" })
    )
    res_json = json.loads(response['Payload'].read().decode("utf-8"))
    response['Payload'] = res_json
    print(response)
    return response

@app.task
def invoke_async(uuid):
    session = boto3.Session(profile_name='racelab')
    client = session.client('lambda')

    response = client.invoke(
        FunctionName='container_tester',
        InvocationType='Event',
        LogType='None',
        Payload=json.dumps({ "messageType" : "work", "invokeType" : "Event", "uuid" : uuid })
    )

    return "Response Status Code : " + str(response['StatusCode'])