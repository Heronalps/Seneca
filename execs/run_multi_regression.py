# The function (run on EC2 instance) creates celery tasks and retrieve result
import sys, os, re, importlib, time, json, copy

# Makes Seneca root directory available for importing
sys.path.insert(0, "./")
from helpers.parsers import parse_path

seneca_path = parse_path(os.getcwd(), "Seneca")
package_path = seneca_path + "/venv/lib/python3.6/site-packages"
sys.path.insert(0, seneca_path)
sys.path.insert(0, package_path)

from celery import group, signature
from proj.tasks import invoke_lambda
import matplotlib.pyplot as plot
from itertools import product
from src.celery_lambda.clean_logs import clean_logs

# This function create all subsets of DATASETS
def create_subset(DATASETS):
    if not DATASETS:
        return []
    final_list = []
    backtrack(DATASETS, 0, [], final_list)
    return final_list

def backtrack(DATASETS, start, temp, final_list):
    for i in range(start, len(DATASETS)):
        temp.append(DATASETS[i])
        final_list.append(copy.deepcopy(temp))
        backtrack(DATASETS, i + 1, temp, final_list)
        del temp[-1]

# This function create json event based on each item in search space
def create_event(config, DATASETS, TARGETS):
    payload_list = []
    subsets = create_subset(DATASETS)    
    for subset in subsets:
        payload = {}
        payload["target_file"] = TARGETS
        payload["variable_files"] = json.dumps(subset)
        payload_list.append(payload)

    return payload_list


# This function create search space of multi_regression and make async request to Lambda

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
    
    # Dynamic importing config file from config_path
    path_prefix, filename = split_path(config_path)
    sys.path.insert(0, path_prefix)
    config = importlib.import_module(filename)
    
    # Dynamic loading lambda name
    LAMBDA_NAME = getattr(config, "LAMBDA_NAME")
    
    # Clean the log of specified lambda function
    clean_logs('/aws/lambda/' + LAMBDA_NAME)

    # Dynamic load parameters 
    DATASETS = []
    TARGETS = getattr(config, 'TARGETS')
    for key in getattr(config, 'DATASETS'):
        DATASETS.append(key)

    # Tune forecast horizon of the chosen model
    payload_list = create_event(config, DATASETS, TARGETS)

    min_metric = float('inf')
    chosen_model_event = None
    metrics = []
    
    from src.lambda_func.multi_regression.multi_regression import lambda_handler
    from contextlib import redirect_stdout

    with open("output.txt", "w") as f:
        with redirect_stdout(f):
            for payload in payload_list:
                print ("======Payload========")
                print (payload)
                map_item = lambda_handler(payload)
                metrics.append(map_item['metric'])
                if map_item['metric'] < min_metric:
                    print ("======Update chosen model event==========")
                    chosen_model_event = map_item['event']
                    min_metric = map_item['metric']
            print ("======Metric=======")
            print (min_metric)
            
            print ("======Event=======")
            print (chosen_model_event)

            print ("======Metrics========")
            print (metrics)

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
    # model_list = saved_result.get()
    # print("===Async Tasks end===")
    
    # for item in model_list:
    #     payload = item['Payload']
    #     if payload['metric'] < min_metric:
    #         chosen_model_event = payload['event']
    #         min_metric = payload['metric']
    
    # print (chosen_model_event)
    # print ("=======The Execution Time===========")
    # print (time.time() - start)

def split_path(path):
    # This regex captures filename after the last backslash
    filename = re.search("(?!\/)(?:.(?!\/))*(?=\.\w*$)", path).group(0)
    path_prefix = re.search("(.*\/)(?!.*\/)", path).group(0)
    
    return path_prefix, filename

if __name__ == "__main__":
    grid_search_controller("./config/multi_regression/config.py")