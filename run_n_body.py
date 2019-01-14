import time, argparse
from proj.tasks import invoke_lambda
from src.celery_lambda.CeleryLambda import CeleryLambda

parser = argparse.ArgumentParser()
parser.add_argument('lambda_name', type=str,
                    help="The name of Lambda function")
parser.add_argument('-c', '--celery_async', action="store_true", 
                    help="turn on to make Celery workers invoke asynchronously")
parser.add_argument('-l', '--lambda_async', action="store_true", 
                    help="turn on to make Lambda is invoked asynchronously")
parser.add_argument('N', type=int, 
                    help="The number of bodies")
parser.add_argument('num_steps', type=int, 
                    help="The number of steps to deduce n-body system")
parser.add_argument('invoke_time', type=int, 
                    help="Total number of invocations")
parser.add_argument('batch_number', type=int,
                    help="Number of batch invocations")
                    
args = parser.parse_args()
print("=====Arguments======")
print("The name of Lambda fucntion = %s" %args.lambda_name)
print("Celery Async = %s" %args.celery_async)
print("Lambda Async = %s" %args.lambda_async)
print("N = %s" %args.N)
print("Number of Steps = %s" %args.num_steps)
print("Number of Invocation = %d" %args.invoke_time)
print("Number of Batch = %d" %args.batch_number)
print("====================")

# print("Warm up call to Lambda container")
# response = invoke_sync("warm-up-call")
# print (response) 
payload = { "N": args.N, "number_of_steps": args.num_steps }

invocation = CeleryLambda(lambda_name = args.lambda_name,
                          celery_async = args.celery_async, 
                          lambda_async = args.lambda_async, 
                          invoke_time = args.invoke_time,
                          batch_number = args.batch_number,
                          sync_payload= payload,
                          async_payload = payload, 
                          decoder = 'utf-8')

invocation.run()

# invocation.sqs_trigger()
