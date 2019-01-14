from celery import group, signature
from datetime import datetime
import time, boto3, json, decimal, argparse, re, pdb
from proj.tasks import invoke_lambda
from src.celery_lambda.clean_logs import clean_logs
from src.celery_lambda.plot import plot_hist
from src.celery_lambda.measurement import show_result

class CeleryLambda:
    def __init__(self, lambda_name, celery_async, lambda_async, invoke_time, 
                 batch_number, sync_payload = {}, async_payload = {}, decoder = {}):
        self.celery_async = celery_async
        self.lambda_async = lambda_async
        self.invoke_time = invoke_time
        self.batch_number = batch_number
        self.lambda_path = "/aws/lambda/" + lambda_name
        self.lambda_name = lambda_name
        self.sync_payload = sync_payload
        self.async_payload = async_payload
        self.decoder = decoder

    def run(self):
        for _n in range(self.batch_number):
            clean_logs(self.lambda_path)

            if (not self.celery_async and not self.lambda_async):
                start_time = time.time()
                for _num in range(self.invoke_time):
                    # print("Lambda is invoked %d time" %(num + 1))
                    invoke_lambda(
                        function_name=self.lambda_name, 
                        sync = True,
                        payload = self.sync_payload,
                        decoder = self.decoder
                    )
                host_execu_time = 1000 * (time.time() - start_time)

            elif (not self.celery_async and self.lambda_async):
                # Add counter to make sure identifier is unique
                start_time = time.time()
                for _num in range(self.invoke_time):
                    # print("Lambda is invoked %d time" %(num + 1))
                    invoke_lambda(
                        function_name = self.lambda_name, 
                        sync = False,
                        payload = self.async_payload
                    )
                host_execu_time = 1000 * (time.time() - start_time)

            elif (self.celery_async and not self.lambda_async):
                start_time = time.time()
                job = group(invoke_lambda.s(
                                function_name = self.lambda_name,
                                sync = True,
                                payload = self.sync_payload,
                                decoder = self.decoder
                                ) for i in range(self.invoke_time))
                print("===Async Tasks start===")
                job.apply_async()
                # result.join()
                host_execu_time = 1000 * (time.time() - start_time)
                print("===Async Tasks end===")
                
            elif (self.celery_async and self.lambda_async):
                start_time = time.time()
                job = group(invoke_lambda.s(
                                function_name = self.lambda_name,
                                sync = False,
                                payload = self.async_payload
                                ) for i in range(self.invoke_time))
                print("===Async Tasks start===")
                result = job.apply_async()
                result.join()
                host_execu_time = 1000 * (time.time() - start_time)
                print("===Async Tasks end===")
            
            time.sleep(25)
            show_result(self.lambda_path, self.celery_async, self.lambda_async, host_execu_time)
            
        # plot_dist(metrics_path, 'total_duration')

    def sqs_trigger(self):
        sqs = boto3.client('sqs')
        invokeType = "Event" if self.lambda_async else "RequestResponse"
        for _i in range(self.batch_number):
            self.identifiers = []
            clean_logs(self.lambda_path)
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
            _response_path, _metrics_path = show_result(self.lambda_path, self.celery_async, self.lambda_async, host_execu_time)