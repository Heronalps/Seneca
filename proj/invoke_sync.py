import json
import boto3
import time
def invoke():
    session = boto3.Session(profile_name='racelab')
    client = session.client('lambda')

    response = client.invoke(
        FunctionName='cold-start-test-js',
        InvocationType='RequestResponse',
        LogType='None',
        Payload=json.dumps({ "messageType" : "work" })
    )
    res_json = json.loads(response['Payload'].read().decode("utf-8"))
    response['Payload'] = res_json
    print(response)
    return response

if __name__ == '__main__':
    invoke()