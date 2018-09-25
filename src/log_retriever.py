import boto3
from helpers.DecimalEncoder import DecimalEncoder 

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

def retrieve_metrics(identifiers):
    total_duration = 0
    total_billed_duration = 0
    max_memory_used = 0
    memory_size = 0
    length = len(identifiers)

    key = 'identifier'
    metrics_table = dynamodb.Table('container_test_metrics')
    

    for id in identifiers:
        response = metrics_table.get_item(
            Key = {key : id}
        )
        
        # print(response)
        total_duration += float(response['Item']['duration'])
        total_billed_duration += float(response['Item']['billed_duration'])
        temp = int(response['Item']['max_memory_used'])
        if temp > max_memory_used:
            max_memory_used = temp
        memory_size = int(response['Item']['memory_size'])
        
    
    duration_per_invocation = total_duration / length
    compute_charge = total_billed_duration * 0.001 * (memory_size / 1024)
    
    # cost = compute charge + request charge
    cost = 0.00001667 * compute_charge + 0.2

    metrics = {
        "total_duration" : total_duration, 
        "total_billed_duration" : total_billed_duration,
        "max_memory_used" : max_memory_used, 
        "memory_size" : memory_size, 
        "duration_per_invocation" : duration_per_invocation, 
        "compute_charge" : compute_charge,
        "cost" : cost
    }

    return metrics    

def retrieve_response(identifiers):
    response_table = dynamodb.Table('container_test_response')
    key = 'identifier'
    
    results = []
    for id in identifiers:
        response = response_table.get_item(
            Key = {key : id}
        )
        results.append(response['Item']['response'])

    return results
    
