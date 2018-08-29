from celery import group, signature
import time, uuid, boto3, json, decimal
from proj.tasks import add, invoke_sync, invoke_async
from multiprocessing.dummy import Pool as ThreadPool 
from boto3.dynamodb.conditions import Key, Attr

celery_sync = False
lambda_sync = True
invokeTime = 12

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table('container_test_table')

def pull_result(id):
    response = table.query(
        KeyConditionExpression = Key('identifier').eq(id)
    )
    for i in response['Items']:
        print(json.dumps(i, cls=DecimalEncoder))


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

if (celery_sync and lambda_sync):
    total_time = 0
    for num in range(invokeTime):
        print("Lambda is invoked %d time" %(num + 1))
        timestamp_start = time.time()
        response = invoke_sync('')
        # response = invoke_sync.delay('')
        # while(not response.ready()):
        #     pass
        # result = response.get()
        total_time += time.time() - timestamp_start
        # print(result)
    print("Time spent : ", total_time)
    print("Invocation times : ", invokeTime)

elif (celery_sync and not lambda_sync):
    total_time = 0
    ids = []
    # Add counter to make sure identifier is unique
    counter = 0
    for num in range(invokeTime):
        identifier = str(uuid.uuid1()) + str(counter)
        counter = counter + 1
        ids.append(identifier)
        print("Lambda is invoked %d time" %(num + 1))
        timestamp_start = time.time()
        response = invoke_async(identifier)
        # response = invoke_async.delay(identifier)
        # while(not response.ready()):
        #     pass
        # result = response.get()
        total_time += time.time() - timestamp_start
        print(response)
        # print(result)
    print("Time spent : ", total_time)
    
    # Pull all responses from DynamoDB
    for id in ids:
        pull_result(id)
    
elif (not celery_sync and lambda_sync):
    job = group(invoke_sync.s('') for i in range(invokeTime))
    print("===Tasks start===")
    timestamp_start = time.time()
    result = job.apply_async()
    r = result.join()
    timestamp_complete = time.time()
    print("===Tasks end===")
    print("Time Spent : ", timestamp_complete - timestamp_start)
    for item in r:
        print(item)

# # In this version, the multithreading is provided by python, not celery 
# elif (not celery_sync and lambda_sync):
#     args = [''] * invokeTime
#     pool = ThreadPool(4)
#     sync_results = pool.map(invoke_sync.delay, args)
#     pool.close()
#     pool.join()
#     print(sync_results)

#     for res in sync_results:
#         print(res.get())

elif (not celery_sync and not lambda_sync):
    ids = []
    # Add counter to make sure identifier is unique
    counter = 0
    for i in range(invokeTime):
        identifier = str(uuid.uuid1()) + str(counter)
        counter = counter + 1
        ids.append(identifier)
        print(identifier)
    
    job = group(invoke_async.s(ids[i]) for i in range(invokeTime))
    print("===Tasks start===")
    timestamp_start = time.time()
    result = job.apply_async()
    r = result.join()
    timestamp_complete = time.time()
    print("===Tasks end===")
    print("Time Spent : ", timestamp_complete - timestamp_start)
    time.sleep(3)
    for item in r:
        print(item)
    # Pull the result from DynamoDB
    for id in ids:
        pull_result(id)