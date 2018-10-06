import boto3, json, pdb
from helpers.DecimalEncoder import DecimalEncoder 
from src.log_parser import parse_log


def retrieve_result(identifiers):
    total_duration = 0
    total_billed_duration = 0
    max_memory_used = 0
    memory_size = 0
    length = len(identifiers)
    response_hash, metrics_hash = parse_log("/aws/lambda/container_tester")

    for id in identifiers:
        metrics = metrics_hash[id]
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

    return response_hash, metrics
    