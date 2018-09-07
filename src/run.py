import time, argparse
from duration import duration
from CeleryLambda import CeleryLambda

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--celery_async', action="store_true", 
                    help="turn on to make Celery workers invoke asynchronously")
parser.add_argument('-l', '--lambda_async', action="store_true", 
                    help="turn on to make Lambda is invoked asynchronously")
parser.add_argument('invoke_time', type=int, 
                    help="Integer value of total number of invocations")
args = parser.parse_args()
print("=====Arguments======")
print("Celery Async = %s" %args.celery_async)
print("Lambda Async = %s" %args.lambda_async)
print("Invoke Time = %d" %args.invoke_time)
print("====================")

timestamp_start = time.time()
invocation = CeleryLambda(celery_async = args.celery_async, lambda_async = args.lambda_async, invoke_time = args.invoke_time)
invocation.run()
timestamp_end = time.time()
print("Start timestamp : ", timestamp_start)
print("End timestamp : ", timestamp_end)
time.sleep(5)
# Available Stat for Lambda: SampleCount, Average, Sum, Minimum, Maximum
response = duration(timestamp_start, timestamp_end, Stat='Sum')
print(response)