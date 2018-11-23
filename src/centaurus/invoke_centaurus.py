from proj.tasks import invoke_centaurus_worker
from src.measurement import show_result
from src.clean_logs import clean_logs
from src.clean_dynamodb import clean_dynamodb
import time, argparse, json

parser = argparse.ArgumentParser()
parser.add_argument('experiment_time', type=int, 
                    help="Number of experiment in one batch")
parser.add_argument('batch_number', type=int,
                    help="Number of batch invocations")
args = parser.parse_args()

print("=====Arguments======")
print("Number of experiment = %d" %args.experiment_time)
print("Number of Batch = %d" %args.batch_number)
print("====================")

payload = json.dumps({
    "n_init": 1,
    "n_exp": args.experiment_time,
    "max_k": 1,
    "covars": [
        "full-tied",
        "full-untied",
        "diag-tied",
        "diag-untied",
        "spher-tied",
        "spher-untied"
    ],
    "columns": [
        "Dimension 1",
        "Dimension 2"
    ],
    "scale": True,
    "s3_file_key": "normal.csv"
})
lambda_name = "/aws/lambda/worker"

for _ in range(args.batch_number):
    print("===Centaurus jobs start===")
    clean_logs(lambda_name)
    clean_dynamodb('kmeansservice', 'job_id', 'task_id')
    
    start_time = time.time()
    invoke_centaurus_worker(payload)
    host_execu_time = 1000 * (time.time() - start_time)
    time.sleep(25)

    show_result(lambda_name, True, True, host_execu_time)
    print("===Centaurus jobs end===")
