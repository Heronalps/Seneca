from celery import group, signature
import time
from proj.tasks import add, invoke_sync, invoke_async
from multiprocessing.dummy import Pool as ThreadPool 

celery_sync = True
lambda_sync = False
invokeTime = 12

if (celery_sync and lambda_sync):
    total_time = 0
    for num in range(invokeTime):
        print("Lambda is invoked %d time" %(num))
        timestamp_start = time.time()
        response = invoke_sync.delay('')
        result = response.get()
        total_time += time.time() - timestamp_start
        print(result)
    print("Time spent : ", total_time)

elif (celery_sync and not lambda_sync):
    total_time = 0
    for num in range(invokeTime):
        print("Lambda is invoked %d time" %(num))
        timestamp_start = time.time()
        response = invoke_async.delay('')
        result = response.get()
        total_time += time.time() - timestamp_start
        print(result)
    # Pull all responses from DynamoDB

    print("Time spent : ", total_time)
elif (not celery_sync and lambda_sync):
    # job = group(add.s(1,1), add.s(2,2))()
    job = group(invoke_sync.s('') for i in range(invokeTime))
    timestamp_start = time.time()
    result = job.apply_async()
    r = result.join()
    timestamp_complete = time.time()
    print("Time Spent : ", timestamp_complete - timestamp_start)
    print(r)

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
    job = group(invoke_async.s('') for i in range(invokeTime))
    timestamp_start = time.time()
    result = job.apply_async()
    r = result.join()
    timestamp_complete = time.time()
    print("Time Spent : ", timestamp_complete - timestamp_start)
    print(r)
    # Pull the result from DynamoDB
    

