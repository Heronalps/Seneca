from celery import group, signature
from datetime import datetime
import time, uuid, boto3, json, decimal, argparse, re, pdb
from helpers.DecimalEncoder import DecimalEncoder 
from proj.tasks import invoke_sync, invoke_async
from src.log_retriever import retrieve_result
from src.clean_logs import clean_logs
from src.plot import plot_dist, plot_hist

class CeleryLambda:
    def __init__(self, celery_async, lambda_async, invoke_time, batch_number):
        self.celery_async = celery_async
        self.lambda_async = lambda_async
        self.invoke_time = invoke_time
        self.batch_number = batch_number
        self.identifiers = []

    def show_result(self, identifiers, host_execu_time):
        group_response, metrics = retrieve_result(identifiers)
        # Print returned values from retrieve_result
        metrics["host_execu_time"] = host_execu_time

        print("===============================Responses=============================")
        for response in group_response:
            print (response)
        
        print("===============================Metrics===============================")
        print("Host Execution Time : %.4f milliseconds" %metrics['host_execu_time'])
        print("Total Time Spent on Lambda : %.4f milliseconds" %metrics['total_duration'])
        print("Invocation Times : %d times" %self.invoke_time)
        print("Time Spent per Invocation : %.4f milliseconds" %metrics['duration_per_invocation'])
        print("Total Billed Duration : %.4f milliseconds" %metrics['total_billed_duration'])
        print("Max Memory Used : %d MBs" %metrics['max_memory_used'])
        print("Memory Allocated : %d MBs" %metrics['memory_size'])
        print("Total Compute Charge : %.4f GB-seconds" %metrics['compute_charge'])
        print("Total Cost : $ %f "%metrics['cost'])
        print("====================================================================")

        # Generate file name with timestamp
        # timestamp = datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
        timestamp = datetime.fromtimestamp(time.time()).strftime('%Y%m%d')
        celery_label = "CA" if self.celery_async else "CS"
        lambda_label = "LA" if self.lambda_async else "LS"
        response_path = "./result/response_" + celery_label + str(self.invoke_time) + lambda_label + "_" + timestamp + ".data"
        metrics_path = "./result/metrics_" + celery_label + str(self.invoke_time) + lambda_label + "_" + timestamp + ".data"
        response_json_str = json.dumps(group_response)
        metrics_json_str = json.dumps(metrics)
        with open(response_path, 'a+') as f:
            f.write(response_json_str + '\n')
        with open(metrics_path, 'a+') as f:
            f.write(metrics_json_str + '\n')

        return response_path, metrics_path

    def generateId(self, counter):
        return str(uuid.uuid1()) + str(counter)

    def run(self):
        for _n in range(self.batch_number):
            self.identifiers = []
            clean_logs("/aws/lambda/container_tester")

            # clean_logs("/aws/lambda/dynamodb_logger")
            if (not self.celery_async and not self.lambda_async):
                start_time = time.time()
                for num in range(self.invoke_time):
                    # print("Lambda is invoked %d time" %(num + 1))
                    identifier = self.generateId(num)
                    self.identifiers.append(identifier)
                    invoke_sync(identifier)
                host_execu_time = 1000 * (time.time() - start_time)

            elif (not self.celery_async and self.lambda_async):
                # Add counter to make sure identifier is unique
                start_time = time.time()
                for num in range(self.invoke_time):
                    # print("Lambda is invoked %d time" %(num + 1))
                    identifier = self.generateId(num)
                    self.identifiers.append(identifier)
                    invoke_async(identifier)
                host_execu_time = 1000 * (time.time() - start_time)

            elif (self.celery_async and not self.lambda_async):
                start_time = time.time()
                for num in range(self.invoke_time):
                    identifier = self.generateId(num)
                    self.identifiers.append(identifier)
                
                # print(self.identifiers)
                job = group(invoke_sync.s(self.identifiers[i]) for i in range(self.invoke_time))
                print("===Async Tasks start===")
                job.apply_async()
                # result.join()
                host_execu_time = 1000 * (time.time() - start_time)
                print("===Async Tasks end===")
                
            elif (self.celery_async and self.lambda_async):
                start_time = time.time()
                for num in range(self.invoke_time):
                    identifier = self.generateId(num)
                    self.identifiers.append(identifier)
                
                # print(self.identifiers)
                job = group(invoke_async.s(self.identifiers[i]) for i in range(self.invoke_time))
                print("===Async Tasks start===")
                job.apply_async()
                # result.join()
                host_execu_time = 1000 * (time.time() - start_time)
                print("===Async Tasks end===")
            
            time.sleep(25)
            _response_path, _metrics_path = self.show_result(self.identifiers, host_execu_time)
        
        # plot_dist(metrics_path, 'total_duration')

    def sqs_trigger(self):
        sqs = boto3.client('sqs')
        invokeType = "Event" if self.lambda_async else "RequestResponse"
        for _i in range(self.batch_number):
            self.identifiers = []
            clean_logs("/aws/lambda/container_tester_sqs")
            start_time = time.time()
            for j in range(self.invoke_time):
                identifier = self.generateId(j)
                self.identifiers.append(identifier)
                body = {
                    "messageType": "refreshConfig",
                    "invokeType": invokeType,
                    "uuid": identifier
                }
                _response = sqs.send_message(
                    QueueUrl='https://sqs.us-west-2.amazonaws.com/603495292017/container-test-queue',
                    MessageBody=json.dumps(body)
                )
            host_execu_time = 1000 * (time.time() - start_time)
            time.sleep(25)
            _response_path, _metrics_path = self.show_result(self.identifiers, host_execu_time)