import boto3

def clean_dynamodb(table_name, primary_key, sort_key=None):
    dynamodb = boto3.resource('dynamodb', 'us-west-2')
    table = dynamodb.Table(table_name)
    attributes = {
        '#p': primary_key,
        '#s': sort_key
    }

    while True:
        scan = table.scan(
            ProjectionExpression='#p, #s',
            ExpressionAttributeNames=attributes
        )
        if not scan['Items']:
            break

        with table.batch_writer() as batch:
            for each in scan['Items']:
                batch.delete_item(Key=each)
