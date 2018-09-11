from celery import group, signature
import time, uuid, boto3, json, decimal, argparse, re
from helpers.DecimalEncoder import DecimalEncoder 
from proj.tasks import add, invoke_sync, invoke_async
from multiprocessing.dummy import Pool as ThreadPool 
from boto3.dynamodb.conditions import Key, Attr
from src.log_retriever import retrieve_metrics, retrieve_response

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
async_response = dynamodb.Table('container_test_async_response')

class CeleryLambda:
    def __init__(self, celery_async, lambda_async, invoke_time):
        self.celery_async = celery_async
        self.lambda_async = lambda_async
        self.invoke_time = invoke_time
        self.requestIds = []

    def pull_result(self, id):
        time.sleep(1)
        response = async_response.get_item(
            Key = {'identifier' : id}
        )
        item = response['Item']['response']
        print(json.dumps(item, cls=DecimalEncoder))

    def show_metrics(self, requestIds, table_name):
        metrics = retrieve_metrics(requestIds, table_name)
        # Print returned values from retrieve_metrics

        print("===============================Metrics===============================")
        print("Total Time Spent : %.4f milliseconds" %metrics['total_duration'])
        print("Invocation Times : %d times" %self.invoke_time)
        print("Time Spent per Invocation : %.4f milliseconds" %metrics['duration_per_invocation'])
        print("Total Billed Duration : %.4f milliseconds" %metrics['total_billed_duration'])
        print("Total Memory Used : %d MBs" %metrics['total_memory_used'])
        print("Memory Allocated : %d MBs" %metrics['memory_size'])
        print("Total Compute Charge : %.4f GB-seconds" %metrics['compute_charge'])
        print("====================================================================")

    def parse_response(self, response):
        requestId = response['ResponseMetadata']['RequestId']
        result = response['Payload']['Message']
        print("requestId : %s " %requestId)
        print("result : %s" %result)
        return requestId

    def run(self):
        if (not self.celery_async and not self.lambda_async):
            for num in range(self.invoke_time):
                print("Lambda is invoked %d time" %(num + 1))
                response = invoke_sync('')
                requestId = self.parse_response(response)
                self.requestIds.append(requestId)
            
            # Wait for metrics to be written into table
            # TODO - Use KeyError to retry until metrics are written

            time.sleep(20)
            self.show_metrics(self.requestIds, 'container_test_metrics')

        elif (not self.celery_async and self.lambda_async):
            # Add counter to make sure identifier is unique
            counter = 0
            for num in range(self.invoke_time):
                identifier = str(uuid.uuid1()) + str(counter)
                counter = counter + 1
                self.requestIds.append(identifier)
                print("Lambda is invoked %d time" %(num + 1))
                response = invoke_async(identifier)
                print(response)
            
            time.sleep(15)
            # Pull all responses from DynamoDB
            results = retrieve_response(self.requestIds, 'container_test_async_response')
            for result in results:
                print(result)
            time.sleep(30)
            self.show_metrics(self.requestIds, 'container_test_async_metrics')

            
        elif (self.celery_async and not self.lambda_async):
            job = group(invoke_sync.s('') for i in range(self.invoke_time))
            print("===Tasks start===")
            timestamp_start = time.time()
            result = job.apply_async()
            r = result.join()
            timestamp_complete = time.time()
            print("===Tasks end===")
            total_time = timestamp_complete - timestamp_start
            self.show_metrics(self.requestIds, 'container_test_metrics')
            for item in r:
                print(item)


        elif (self.celery_async and self.lambda_async):
            ids = []
            # Add counter to make sure identifier is unique
            counter = 0
            for _i in range(self.invoke_time):
                identifier = str(uuid.uuid1()) + str(counter)
                counter = counter + 1
                ids.append(identifier)
            
            job = group(invoke_async.s(ids[i]) for i in range(self.invoke_time))
            print("===Tasks start===")
            timestamp_start = time.time()
            result = job.apply_async()
            r = result.join()
            timestamp_complete = time.time()
            print("===Tasks end===")
            total_time = timestamp_complete - timestamp_start
            self.show_metrics(self.requestIds, 'container_test_async_metrics')
            for item in r:
                print(item)
            # Pull the result from DynamoDB
            