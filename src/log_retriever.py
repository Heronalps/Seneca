import boto3, json
from helpers.DecimalEncoder import DecimalEncoder 

s3 = boto3.resource('s3', region_name='us-west-2')
metrics_bucket = 'container-test-metrics'
response_bucket = 'container-test-response'

def retrieve_metrics(identifiers):
    total_duration = 0
    total_billed_duration = 0
    max_memory_used = 0
    memory_size = 0
    length = len(identifiers)

    for id in identifiers:
        object = s3.Object(metrics_bucket, id)
        response = object.get()['Body'].read().decode("utf-8")
        metrics = json.loads(response)
        
        # print(response)
        total_duration += float(metrics['duration'])
        total_billed_duration += float(metrics['billed_duration'])
        temp = int(metrics['max_memory_used'])
        if temp > max_memory_used:
            max_memory_used = temp
        memory_size = int(metrics['memory_size'])
        
    
    duration_per_invocation = total_duration / length
    compute_charge = total_billed_duration * 0.001 * (memory_size / 1024)
    
    # cost = compute charge + request charge
    cost = 0.00001667 * compute_charge

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
    results = []
    for id in identifiers:
        object = s3.Object(response_bucket, id)
        response = object.get()['Body'].read().decode("utf-8")
        results.append(response)

    return results
    
# def iterate_bucket_items(bucket):
#     """
#     Generator that iterates over all objects in a given s3 bucket
#     """

#     client = boto3.client('s3')
#     paginator = client.get_paginator('list_objects_v2')
#     page_iterator = paginator.paginate(Bucket=bucket)

#     for page in page_iterator:
#         for item in page['Contents']:
#             yield item