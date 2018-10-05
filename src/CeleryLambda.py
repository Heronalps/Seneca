from celery import group, signature
import time, uuid, boto3, json, decimal, argparse, re
from helpers.DecimalEncoder import DecimalEncoder 
from proj.tasks import add, invoke_sync, invoke_async
from multiprocessing.dummy import Pool as ThreadPool 
from boto3.dynamodb.conditions import Key, Attr
from src.log_retriever import retrieve_metrics, retrieve_response

class CeleryLambda:
    def __init__(self, celery_async, lambda_async, invoke_time):
        self.celery_async = celery_async
        self.lambda_async = lambda_async
        self.invoke_time = invoke_time
        self.identifiers = []

    def show_metrics(self, identifiers, host_execu_time):
        metrics = retrieve_metrics(identifiers)
        # Print returned values from retrieve_metrics

        print("===============================Metrics===============================")
        print("Host Executione Time : %.4f milliseconds" %host_execu_time)
        print("Total Time Spent on Lambda : %.4f milliseconds" %metrics['total_duration'])
        print("Invocation Times : %d times" %self.invoke_time)
        print("Time Spent per Invocation : %.4f milliseconds" %metrics['duration_per_invocation'])
        print("Total Billed Duration : %.4f milliseconds" %metrics['total_billed_duration'])
        print("Max Memory Used : %d MBs" %metrics['max_memory_used'])
        print("Memory Allocated : %d MBs" %metrics['memory_size'])
        print("Total Compute Charge : %.4f GB-seconds" %metrics['compute_charge'])
        print("Total Cost : $ %f "%metrics['cost'])
        print("====================================================================")

    def generateId(self, counter):
        return str(uuid.uuid1()) + str(counter)

    def run(self):
        self.identifiers = []
        if (not self.celery_async and not self.lambda_async):
            start_time = time.time()
            for num in range(self.invoke_time):
                print("Lambda is invoked %d time" %(num + 1))
                identifier = self.generateId(num)
                response = invoke_sync(identifier)
                # print (response)
                self.identifiers.append(identifier)
            host_execu_time = 1000 * (time.time() - start_time)
            
            # Wait for metrics to be written into table
            # TODO - Use KeyError to retry until metrics are written

            time.sleep(20)
            self.show_metrics(self.identifiers, host_execu_time)

        elif (not self.celery_async and self.lambda_async):
            # Add counter to make sure identifier is unique
            start_time = time.time()
            for num in range(self.invoke_time):
                identifier = self.generateId(num)
                self.identifiers.append(identifier)
                print("Lambda is invoked %d time" %(num + 1))
                response = invoke_async(identifier)
                # print(response)
            host_execu_time = 1000 * (time.time() - start_time)
            print(self.identifiers)
            time.sleep(20)
            # Pull all responses from DynamoDB
            results = retrieve_response(self.identifiers)
            for result in results:
                print(result)
            time.sleep(15)
            self.show_metrics(self.identifiers, host_execu_time)

        elif (self.celery_async and not self.lambda_async):
            start_time = time.time()
            for num in range(self.invoke_time):
                identifier = self.generateId(num)
                self.identifiers.append(identifier)
            
            print(self.identifiers)
            job = group(invoke_sync.s(self.identifiers[i]) for i in range(self.invoke_time))
            print("===Tasks start===")
            result = job.apply_async()
            host_execu_time = 1000 * (time.time() - start_time)
            print("===Tasks end===")
            time.sleep(30)
            self.show_metrics(self.identifiers, host_execu_time)
            
        elif (self.celery_async and self.lambda_async):
            start_time = time.time()
            for num in range(self.invoke_time):
                identifier = self.generateId(num)
                self.identifiers.append(identifier)
            
            print(self.identifiers)
            job = group(invoke_async.s(self.identifiers[i]) for i in range(self.invoke_time))
            print("===Tasks start===")
            result = job.apply_async()
            host_execu_time = 1000 * (time.time() - start_time)
            print("===Tasks end===")
            time.sleep(30)
            self.show_metrics(self.identifiers, host_execu_time)
            responses = retrieve_response(self.identifiers)
            for response in responses:
                print (response)
            