 # The function (run on EC2 instance) creates celery tasks and retrieve result
import sys, os, re, importlib, time
# Makes Seneca root directory available for importing
sys.path.insert(0, "./")
from helpers.parsers import parse_path
from helpers.parsers import split_path
from helpers.module_loader import load

seneca_path = parse_path(os.getcwd(), "Seneca")
package_path = seneca_path + "/venv/lib/python3.6/site-packages"
sys.path.insert(0, seneca_path)
sys.path.insert(0, package_path)

from celery import group, signature
from proj.tasks import invoke_lambda
import matplotlib.pyplot as plot
from itertools import product
from src.celery_lambda.clean_logs import clean_logs

# This function create json event based on each item in search space
def create_event(config, PARAMETERS, CONFIG):
    
    # Search for model with Cartisan Product of hyperparameters
    parameter_lists = []
    for parameter in PARAMETERS:
        parameter_lists.append(getattr(config.Hyperparameter, parameter))
    search_space = product(*parameter_lists)

    payload_list = []
    for item in search_space:
        payload = {}
        payload['parameters'] = [key.lower() for key in (PARAMETERS)]
        payload['data'] = {}
        # Transfer tuple to list, because zip() requires list as argument
        for key, value in zip(PARAMETERS, list(item)):
            payload['data'][key.lower()] = value
            
        payload['dataset'] = getattr(config.Config, 'DATASET')
        payload['test_size'] = getattr(config.Config, 'TEST_SIZE')    
        payload_list.append(payload)

    return payload_list

# This function create search space of prophet modeling and make async request to Lambda

'''
    Paramters:
        config_path
    Returns:
        Forecast graph with chosen model
    Process:
        Model training -> cross validation under <initial, period, horizon> 
        -> Forecast graph / dataframe
'''

def grid_search_controller(config_path):
    start = time.time()
    # Dynamic importing config file from config_path
    config = load(config_path)
    
    # Dynamic loading lambda name
    LAMBDA_NAME = getattr(config.Config, "LAMBDA_NAME")
    
    # Clean the log of specified lambda function
    # clean_logs('/aws/lambda/' + LAMBDA_NAME)

    # Dynamic load parameters 
    PARAMETERS = []
    CONFIG = []
    for key in dir(config.Hyperparameter):
        if key.isupper():
            PARAMETERS.append(key)
    for key in dir(config.Config):
        if key.isupper():
            CONFIG.append(key)

    # Tune forecast horizon of the chosen model
    payload_list = create_event(config, PARAMETERS, CONFIG)

    max_metric = float('-inf')
    chosen_model_event = None
    metrics = []
    from src.lambda_func.svc.svc import lambda_handler
    from contextlib import redirect_stdout
    with open("./svc_output.txt", "w") as f:
        with redirect_stdout(f):
            for payload in payload_list:
                map_item = lambda_handler(payload)
                # Metric is Accuracy Score => Large than
                metrics.append(map_item['metric'])
                if map_item['metric'] > max_metric:
                    print ("======Update chosen model event==========")
                    chosen_model_event = map_item['event']
                    max_metric = map_item['metric']
            print ("====Max Accuracy Score=====")        
            print (max_metric)
            print ("====Event============")
            print (chosen_model_event)
            print ("====Metrics List=====")
            print (metrics)
            print ("====Execution time=====")
            print (time.time() - start)
    # start = time.time()
    # print ("=====Time Stamp======")
    # print (start)
    # job = group(invoke_lambda.s(
    #                 function_name = LAMBDA_NAME,
    #                 sync = True,
    #                 payload = payload
    #                 ) for payload in payload_list)
    # print("===Async Tasks start===")
    # result = job.apply_async()
    # result.save()
    # from celery.result import GroupResult
    # saved_result = GroupResult.restore(result.id)

    # while not saved_result.ready():
    #     time.sleep(0.1)
    # model_list = saved_result.get(timeout=None)
    
    
    # print("===Async Tasks end===")
    # print (time.time() - start)
    
    # for item in model_list:
    #     payload = item['Payload']
    #     # Metric is Accuracy Score => Large than
    #     if payload['metric'] > max_metric:
    #         chosen_model_event = payload['event']
    #         max_metric = payload['metric']
    
    # print (max_metric)
    # print (chosen_model_event)

    # from src.celery_lambda import measurement
    # measurement.parse_log("/aws/lambda/svc_worker")

if __name__ == "__main__":
    path = "/Users/michaelzhang/Downloads/Seneca/config/svc/config.py"
    grid_search_controller(path)