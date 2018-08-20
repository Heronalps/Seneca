from celery import group, signature
import time
from proj.tasks import add, invoke_sync, invoke_async
from multiprocessing.dummy import Pool as ThreadPool 

celery_sync = True
lambda_sync = False
invokeTime = 12

if (celery_sync and lambda_sync):
    for num in range(5):
        response = invoke_sync.delay('')
        print("Lambda is invoked %d time" %(num))
        result = response.get()
        print(result)
elif (celery_sync and not lambda_sync):
    for num in range(5):
        response = invoke_async.delay('')
        print("Lambda is invoked %d time" %(num))
        result = response.get()
        print(result)
# elif (not celery_sync and lambda_sync):
#     # job = group(add.s(1,1), add.s(2,2))()
#     job = group(invoke_sync.s('') for i in range(invokeTime))
#     print(job)
#     result = job.apply_async()
#     print(result)
#     print(result.ready())
#     print(result.successful())
#     while not result.ready():
#         print("Retry")
#         r = result.join()
#         # time.sleep(1)
#     print(r)

elif (not celery_sync and lambda_sync):
    args = [''] * invokeTime
    pool = ThreadPool(4)
    sync_results = pool.map(invoke_sync.delay, args)
    pool.close()
    pool.join()
    print(sync_results)

    for res in sync_results:
        print(res.get())