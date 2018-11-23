import boto3, json

sqs = boto3.client('sqs')
body = {
  "messageType": "refreshConfig",
  "invokeType": "Event",
  "uuid": "abcd"
}
response = sqs.send_message(
    QueueUrl='https://sqs.us-west-2.amazonaws.com/603495292017/container-test-queue',
    MessageBody=json.dumps(body)
)
print (response)