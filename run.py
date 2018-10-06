import time, argparse
from src.CeleryLambda import CeleryLambda
from src.clean_logs import clean_logs
from src.clean_s3_objects import clean_objects
from proj.tasks import add, invoke_sync, invoke_async

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--celery_async', action="store_true", 
                    help="turn on to make Celery workers invoke asynchronously")
parser.add_argument('-l', '--lambda_async', action="store_true", 
                    help="turn on to make Lambda is invoked asynchronously")
parser.add_argument('invoke_time', type=int, 
                    help="Integer value of total number of invocations")
parser.add_argument('batch_time', type=int,
                    help="Number of batch invocations")
args = parser.parse_args()
print("=====Arguments======")
print("Celery Async = %s" %args.celery_async)
print("Lambda Async = %s" %args.lambda_async)
print("Number of Invocation = %d" %args.invoke_time)
print("Number of Batch = %d" %args.batch_time)
print("====================")

print("Warm up call to Lambda container")
response = invoke_sync("warm-up-call")
print (response) 

invocation = CeleryLambda(celery_async = args.celery_async, lambda_async = args.lambda_async, invoke_time = args.invoke_time)
for _i in range(args.batch_time):
    clean_logs("/aws/lambda/container_tester")
    clean_logs("/aws/lambda/dynamodb_logger")
    clean_objects("container-test-response")
    clean_objects("container-test-metrics")
    invocation.run()