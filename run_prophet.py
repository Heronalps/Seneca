# The function (run on EC2 instance) creates celery tasks and retrieve result

from celery import group, signature
from proj.tasks import invoke_lambda
import matplotlib.pyplot as plot
from config import model_config, cross_validation_config
from itertools import product
from src.celery_lambda.clean_logs import clean_logs
from src.lambda_func.prophet import grid_search_worker

LAMBDA_NAME = 'prophet_worker'
FORECAST = '360'
PARAMETERS = ['GROWTH', 'CAP', 'FLOOR', 'CHANGEPOINT_PRIOR_SCALE', 'HOLIDAYS',
              'COUNTRY_HOLIDAYS', 'HOLIDAYS_PRIOR_SCALE', 'FOURIER_ORDER', 'SEASONALITY_PRIOR_SCALE', 
              'SEASONALITY_MODE', 'INTERVAL_WIDTH', 'MCMC_SAMPLES', 'LEFT_BOUND', 'RIGHT_BOUND']

CV_SETTINGS = ['INITIAL', 'PERIOD', 'HORIZON', 'METRIC']

# This function create json event based on each item in search space
def create_event(search_space):
    payload_list = []
    for item in search_space:
        payload = {}
        for i, j in zip(PARAMETERS, list(item)):
            payload[i.lower()] = j
        for item in CV_SETTINGS:
            payload[item.lower()] = getattr(cross_validation_config, item)
        
        # Zero forecast period makes lambda cross validation
        payload['forecast'] = 0    
        
        payload_list.append(payload)
    return payload_list

# This function create search space of prophet modeling and make async request to Lambda

'''
    Paramters:
        model_config
        cross_validation_config
        forecast_period
    Returns:
        Forecast graph with chosen model
    Process:
        Model training -> cross validation under <initial, period, horizon> 
        -> Forecast graph / dataframe
'''

def grid_search_controller():
    clean_logs('/aws/lambda/' + LAMBDA_NAME)
    # Search for model with Cartisan Product of hyperparameters
    parameter_lists = []
    
    for parameter in PARAMETERS:
        parameter_lists.append(getattr(model_config, parameter))
    search_space = product(*parameter_lists)
    
    # Tune forecast horizon of the chosen model
    payload_list = create_event(search_space)

    max_metric = float('inf')
    chosen_model_event = None

    # for payload in payload_list:
    #     map_item = grid_search_worker(payload)
    #     if map_item['average_metric'] < max_metric:
    #         print ("======Update chosen model event==========")
    #         chosen_model_event = map_item['event']
    
    job = group(invoke_lambda.s(
                    function_name = LAMBDA_NAME,
                    sync = True,
                    payload = payload
                    ) for payload in payload_list)
    print("===Async Tasks start===")
    result = job.apply_async()
    result.join_native(timeout=None)
    model_list = result.get()
    print("===Async Tasks end===")
    # import pdb; pdb.set_trace();
    for item in model_list:
        payload = item['Payload']
        if payload['average_metric'] < max_metric:
            chosen_model_event = payload['event']
    
    # Non-zero forecast period makes lambda upload graphs to s3
    chosen_model_event['forecast'] = FORECAST
    
    # Invoke Lambda with forecast

    response = invoke_lambda(function_name = LAMBDA_NAME,
                             sync=True,
                             payload=chosen_model_event)
    print (response)

if __name__ == "__main__":
    grid_search_controller()