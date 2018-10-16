from celery import group, signature
from datetime import datetime
import time, boto3, json, decimal, argparse, re, pdb
from proj.tasks import invoke_sync, invoke_async
from src.clean_logs import clean_logs
from src.plot import plot_dist, plot_hist
from src.measurement import show_result

class CeleryLambda:
    def __init__(self, lambda_name, celery_async, lambda_async, invoke_time, batch_number):
        self.celery_async = celery_async
        self.lambda_async = lambda_async
        self.invoke_time = invoke_time
        self.batch_number = batch_number
        self.lambda_name = "/aws/lambda/" + lambda_name

    def run(self):
        for _n in range(self.batch_number):
            clean_logs(self.lambda_name)

            if (not self.celery_async and not self.lambda_async):
                start_time = time.time()
                for _num in range(self.invoke_time):
                    # print("Lambda is invoked %d time" %(num + 1))
                    invoke_sync()
                host_execu_time = 1000 * (time.time() - start_time)

            elif (not self.celery_async and self.lambda_async):
                # Add counter to make sure identifier is unique
                start_time = time.time()
                for _num in range(self.invoke_time):
                    # print("Lambda is invoked %d time" %(num + 1))
                    invoke_async()
                host_execu_time = 1000 * (time.time() - start_time)

            elif (self.celery_async and not self.lambda_async):
                start_time = time.time()
                job = group(invoke_sync.s() for i in range(self.invoke_time))
                print("===Async Tasks start===")
                job.apply_async()
                # result.join()
                host_execu_time = 1000 * (time.time() - start_time)
                print("===Async Tasks end===")
                
            elif (self.celery_async and self.lambda_async):
                start_time = time.time()
                job = group(invoke_async.s() for i in range(self.invoke_time))
                print("===Async Tasks start===")
                job.apply_async()
                # result.join()
                host_execu_time = 1000 * (time.time() - start_time)
                print("===Async Tasks end===")
            
            time.sleep(25)
            show_result(self.lambda_name, self.celery_async, self.lambda_async, host_execu_time)
            
        # plot_dist(metrics_path, 'total_duration')

    def sqs_trigger(self):
        sqs = boto3.client('sqs')
        invokeType = "Event" if self.lambda_async else "RequestResponse"
        for _i in range(self.batch_number):
            self.identifiers = []
            clean_logs(self.lambda_name)
            start_time = time.time()
            for _j in range(self.invoke_time):
                body = {
                    "messageType": "refreshConfig",
                    "invokeType": invokeType
                }
                _response = sqs.send_message(
                    QueueUrl='https://sqs.us-west-2.amazonaws.com/603495292017/container-test-queue',
                    MessageBody=json.dumps(body)
                )
            host_execu_time = 1000 * (time.time() - start_time)
            time.sleep(25)
            _response_path, _metrics_path = show_result(self.lambda_name, self.celery_async, self.lambda_async, host_execu_time)