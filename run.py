from proj.tasks import add, invoke_sync, invoke_async
from multiprocessing.dummy import Pool as ThreadPool 

celery_sync = True 
lambda_sync = True
invokeTime = 8

if (celery_sync and lambda_sync):
    for num in range(5):
        response = invoke_sync.delay('')
        print("Lambda is invoked %d time" %(num))
        result = response.get()
        print(result)
elif (not celery_sync and lambda_sync):
    args = []    
    for i in range(invokeTime):
        args.append(str(i))

    pool = ThreadPool(4)

    async_results = pool.map(invoke_sync, args)
    pool.close()
    pool.join()

    for res in async_results:
        
        res.get()