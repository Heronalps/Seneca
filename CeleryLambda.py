from celery import group, signature
import time, uuid, boto3, json, decimal, argparse
from duration import duration
from helpers.DecimalEncoder import DecimalEncoder 
from proj.tasks import add, invoke_sync, invoke_async
from multiprocessing.dummy import Pool as ThreadPool 
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table('container_test_table')

class CeleryLambda:
    def __init__(self, celery_async, lambda_async, invoke_time):
        self.celery_async = celery_async
        self.lambda_async = lambda_async
        self.invoke_time = invoke_time
        self.responses = []

    def pull_result(self, id):
        time.sleep(3)
        response = table.get_item(
            Key = {'identifier' : id}
        )
        item = response['Item']['response']
        self.responses.append(item)
        print(json.dumps(item, cls=DecimalEncoder))

    def print_result(self, total_time, invoke_time):
        print("===============================RESULT===============================")
        print("Total Time Spent : %.4f seconds" %total_time)
        print("Invocation Times : %d times" %invoke_time)
        print("Time Spent per Invocation : %.4f seconds" %(total_time / invoke_time))
        print("====================================================================")

    def get_time_range(self):
        for r in self.responses:
            print("====Response====")
            print(r)

    def run(self):
        if (not self.celery_async and not self.lambda_async):
            total_time = 0
            for num in range(self.invoke_time):
                print("Lambda is invoked %d time" %(num + 1))
                timestamp_start = time.time()
                response = invoke_sync('')
                self.responses.append(response['Payload'])
                total_time += time.time() - timestamp_start

            self.print_result(total_time, self.invoke_time)
            return self.get_time_range()

        elif (not self.celery_async and self.lambda_async):
            total_time = 0
            ids = []
            # Add counter to make sure identifier is unique
            counter = 0
            for num in range(self.invoke_time):
                identifier = str(uuid.uuid1()) + str(counter)
                counter = counter + 1
                ids.append(identifier)
                print("Lambda is invoked %d time" %(num + 1))
                timestamp_start = time.time()
                response = invoke_async(identifier)
                total_time += time.time() - timestamp_start
                print(response)
            self.print_result(total_time, self.invoke_time)
            
            # Pull all responses from DynamoDB
            for id in ids:
                self.pull_result(id)

            return self.get_time_range()
            
        elif (self.celery_async and not self.lambda_async):
            job = group(invoke_sync.s('') for i in range(self.invoke_time))
            print("===Tasks start===")
            timestamp_start = time.time()
            result = job.apply_async()
            r = result.join()
            timestamp_complete = time.time()
            print("===Tasks end===")
            total_time = timestamp_complete - timestamp_start
            self.print_result(total_time, self.invoke_time)
            for item in r:
                print(item)
                self.responses.append(item['Payload'])

            return self.get_time_range()

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
            self.print_result(total_time, self.invoke_time)
            for item in r:
                print(item)
            # Pull the result from DynamoDB
            for id in ids:
                self.pull_result(id)

            return self.get_time_range()