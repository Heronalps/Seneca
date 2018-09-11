import boto3
from helpers.DecimalEncoder import DecimalEncoder 

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

def retrieve_metrics(requestIds, table_name):
    total_duration = 0
    total_billed_duration = 0
    total_memory_used = 0
    memory_size = 0
    length = len(requestIds)

    key = ''
    metrics_table = dynamodb.Table(table_name)
    if table_name == 'container_test_async_metrics':
        key = 'identifier'
    elif table_name == 'container_test_metrics':
        key = 'requestId'
    
    for id in requestIds:
        response = metrics_table.get_item(
            Key = {key : id}
        )
        
        total_duration += float(response['Item']['duration'])
        total_billed_duration += float(response['Item']['billed_duration'])
        total_memory_used = int(response['Item']['max_memory_used'])
        memory_size = int(response['Item']['memory_size'])
        
    
    duration_per_invocation = total_duration / length
    compute_charge = total_billed_duration * (memory_size / 1024)
    metrics = {
        "total_duration" : total_duration, 
        "total_billed_duration" : total_billed_duration,
        "total_memory_used" : total_memory_used, 
        "memory_size" : memory_size, 
        "duration_per_invocation" : duration_per_invocation, 
        "compute_charge" : compute_charge
    }

    return metrics    

def retrieve_response(requestIds, table_name):
    response_table = dynamodb.Table(table_name)
    key = ''
    if table_name == 'container_test_async_response':
        key = 'identifier'
    elif table_name == 'container_test_response':
        key = 'requestId'

    results = []
    for id in requestIds:
        response = response_table.get_item(
            Key = {key : id}
        )
        results.append(response['Item']['response'])

    return results
    
