import json, boto3, time

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