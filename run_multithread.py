from proj.tasks import add, invoke_sync
import time
from multiprocessing.dummy import Pool as ThreadPool 

args = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

pool = ThreadPool(4)

sync_results = pool.map(invoke_sync, args)
pool.close()
pool.join()

# for res in sync_results:
#     time.sleep(3)
#     print(res.get())