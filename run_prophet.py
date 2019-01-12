# The function (run on EC2 instance) creates celery tasks and retrieve result

from config import model_config, cross_validation_config
from itertools import product
from celery import group, signature
from proj.tasks import invoke_lambda
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
LAMBDA_NAME = ''
PARAMETERS = ['GROWTH', 'CAP', 'FLOOR', 'CHANGEPOINT_PRIOR_SCALE', 'COUNTRY_HOLIDAYS', 
              'HOLIDAYS_PRIOR_SCALE', 'FOURIER_ORDER', 'SEASONALITY_PRIOR_SCALE', 
              'SEASONALITY_MODE', 'INTERVAL_WIDTH']

# This function create json event based on each item in search space
def create_event(search_space):
    payload_list = []
    for item in search_space:
        payload = {}
        for i, j in zip(PARAMETERS, list(item)):
            payload[i.lower()] = j
        print (payload)
        payload_list.append(payload)
    return payload_list

# This function create search space of prophet modeling and make async request to Lambda
def grid_search_controller():
    # Search for model with Cartisan Product of hyperparameters
    parameter_lists = []
    
    for parameter in PARAMETERS:
        parameter_lists.append(getattr(model_config, parameter))
        print ("=====Value List=====")
        print (parameter_lists)
    search_space = product(*parameter_lists)
    # Tune forecast horizon of the chosen model
    payload_list = create_event(search_space)

    job = group(invoke_lambda.s(
                    function_name = LAMBDA_NAME,
                    sync = True,
                    payload = payload
                    ) for payload in payload_list)
    print("===Async Tasks start===")
    job.apply_async()
    # result.join()
    print("===Async Tasks end===")
    
if __name__ == "__main__":
    grid_search_controller()