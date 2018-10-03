import json
import boto3
import time
def invoke():
    session = boto3.Session(profile_name='racelab')
    client = session.client('lambda')

    response = client.invoke(
        FunctionName='cold-start-test-js',
        InvocationType='Event',
        LogType='None',
        Payload=json.dumps({ "messageType" : "work" })
    )

    print("Response Status Code : " + str(response['StatusCode']))

if __name__ == '__main__':
    invoke()