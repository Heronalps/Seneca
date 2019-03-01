import boto3, botocore, json, base64, re, math, collections, os

Config = botocore.config.Config(connect_timeout=900, read_timeout=900)
client = boto3.client("lambda", config=Config)

class Optimizer():
    def __init__(self, fn_name, payload):
        self.fn_name = fn_name
        self.AWS_ROLE = os.environ['AWS_ROLE']

        # The max length of queue used for monotonically increase decision
        self.QUEUE_MAX_LEN = 5
        self.SLOPE_INCREASE = 1

        # This input could possibly impact the outocome of optimization, 
        # meaning the varying parameter could lead to different sweetspot in the real-world execution.
        self.payload = payload

    def create_function(self, fn_name, AWS_ROLE):
        functions = client.list_functions()['Functions']
        created = False
        for func in functions:
            if func['FunctionName'] == fn_name:
                created = True
                # Initialize function allcoted memory as maximum 
                # to explore Max Used Memory as starting point
                self.update_config(fn_name, 3008)
                print("Function {0} has been created!".format(fn_name))
        
        if not created:
            print("Function has not been created yet!")
            client.create_function(
                FunctionName= fn_name,
                Runtime= "python3.6",
                Role= AWS_ROLE,
                Handler= "{0}.lambda_handler".format(fn_name),
                Code={ 'ZipFile' : open("{0}.zip".format(fn_name), 'rb').read()},
                
                # Initialize function allcoted memory as maximum 
                # to explore Max Used Memory as starting point
                MemorySize= 3008
            )
            # print(response)

    def invoke(self, fn_name, payload):
        response = client.invoke(
            FunctionName = fn_name,
            InvocationType = 'RequestResponse',
            LogType = 'Tail',
            Payload = payload
        )
        
        # request_id = response['ResponseMetadata']['RequestId']
        log_string = base64.b64decode(response['LogResult']).decode('utf-8')
        billed_duration = int(re.search(r'(?<=\tBilled\sDuration:\s)(.*?)(?=\sms)', log_string).group(0))
        memory_size = int(re.search(r'(?<=\tMemory\sSize:\s)(.*?)(?=\sMB)', log_string).group(0))
        max_memory_used = int(re.search(r'(?<=\tMax\sMemory\sUsed:\s)(.*?)(?=\sMB)', log_string).group(0))
        
        # The flag of the lower bound of lambda function
        process_exit = True if re.search(r'Process exited before completing request', log_string) else False
        compute_charge = billed_duration * 1e-3 * memory_size / 1024
        # print("===Log String===")
        # print (log_string)
        # print("===Computing Charge===")
        # print(compute_charge)
        # print("======")
        metrics = {
            "billed_duration" : billed_duration,
            "max_memory_used" : max_memory_used,
            "memory_size" : memory_size,
            "compute_charge" : compute_charge,
            "process_exit" : process_exit
        }
        return metrics

    def update_config(self, fn_name, memory_size):
        print("update allocated memory to {0} MB".format(memory_size))
        client.update_function_configuration(
            FunctionName = fn_name,
            MemorySize = memory_size
        )

    # This function optimizes the allocated memory of Lambda by linear search
    # due to the fluctuation of the compute charge. It literally tries out 
    # allocated memory from the upper bound (3008 MB) to lower bound able to 
    # execute lambda function.

    def run(self):
        self.create_function(self.fn_name, self.AWS_ROLE)
        metrics = self.invoke(self.fn_name, self.payload)
        starting_point = math.ceil(metrics['max_memory_used'] / 64)
        if starting_point == 1: 
            starting_point = starting_point + 1
        print ("======Starting Point==========")
        print (starting_point)
        
        # If no sweetspot is found, the lambda function will be configured to 128MB
        # in order to save compute charge.
        allocated_memory = starting_point * 64
        
        prev_memory = collections.deque(maxlen = self.QUEUE_MAX_LEN)
        prev_compute_charge = collections.deque(maxlen = self.QUEUE_MAX_LEN)
        optimization_cost = 0.0
        min_compute_charge = float('inf')

        # Search from starting point of lower bound to sweet spot
        for num in range (starting_point, 48, 1): 
            self.update_config(self.fn_name, num * 64)
            metrics = self.invoke(self.fn_name, self.payload)
            optimization_cost = optimization_cost + metrics['compute_charge'] * 0.00001667
            if metrics['process_exit']:
                continue
            print ("Current compute charge = {0}".format(metrics['compute_charge']))
            print ("Total compute charge = {0}".format(optimization_cost))

            # Keep the allocated memory from minimum compute charge 
            if metrics['compute_charge'] < min_compute_charge:
                min_compute_charge = metrics['compute_charge']
                allocated_memory = num * 64
            prev_compute_charge.append(metrics['compute_charge'])
            prev_memory.append(num * 64)
            
            # If the sweetspot is found, update the allocated memory
            if (self.isSweetspot(prev_compute_charge)):
                if prev_memory[0] < min_compute_charge:
                    allocated_memory = prev_memory.popleft() 
                break

        self.update_config(self.fn_name, allocated_memory)
        print ("The lambda function has been configured at {0} MB as allocated memory!".format(allocated_memory))
        print ("The cost of optimizing lambda function is ${0} !".format(optimization_cost))

    # Ideally, the user should specify a lambda deployment package and this script
    # will optimize the function configuration for you.

    def isSweetspot(self, time_series):
        if time_series.maxlen != len(time_series):
            return False
        
        flag = True
        prev = 0.0
        # Verify if the whole list monotonically increase
        for ts in time_series:
            if ts <= prev:
                flag = False
            else:
                prev = ts
        # Verify if the slope of list greater than SLOPE_INCREASE
        slope = (time_series[-1] - time_series[0]) / time_series.maxlen
        if slope < self.SLOPE_INCREASE:
            flag = False
        return flag

if __name__ == "__main__":
    optimizer = Optimizer(fn_name = "random_num_workload", 
                          payload = json.dumps({ "number" : "10" }))
    optimizer.run()