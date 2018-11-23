import time, argparse
from src.CeleryLambda import CeleryLambda
from proj.tasks import invoke_sync, invoke_async

parser = argparse.ArgumentParser()
parser.add_argument('lambda_name', type=str,
                    help="The name of Lambda function")
parser.add_argument('-c', '--celery_async', action="store_true", 
                    help="turn on to make Celery workers invoke asynchronously")
parser.add_argument('-l', '--lambda_async', action="store_true", 
                    help="turn on to make Lambda is invoked asynchronously")
parser.add_argument('invoke_time', type=int, 
                    help="Integer value of total number of invocations")
parser.add_argument('batch_number', type=int,
                    help="Number of batch invocations")
                    
args = parser.parse_args()
print("=====Arguments======")
print("The name of Lambda fucntion = %s" %args.lambda_name)
print("Celery Async = %s" %args.celery_async)
print("Lambda Async = %s" %args.lambda_async)
print("Number of Invocation = %d" %args.invoke_time)
print("Number of Batch = %d" %args.batch_number)
print("====================")

# print("Warm up call to Lambda container")
# response = invoke_sync("warm-up-call")
# print (response) 

invocation = CeleryLambda(lambda_name = args.lambda_name,
                          celery_async = args.celery_async, 
                          lambda_async = args.lambda_async, 
                          invoke_time = args.invoke_time,
                          batch_number = args.batch_number)
invocation.run()
# invocation.sqs_trigger()