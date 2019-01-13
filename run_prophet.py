# The function (run on EC2 instance) creates celery tasks and retrieve result

from celery import group, signature
from proj.tasks import invoke_lambda
import matplotlib.pyplot as plot
from config import model_config, cross_validation_config
from itertools import product

LAMBDA_NAME = ''
FORECAST = '360'
PARAMETERS = ['GROWTH', 'CAP', 'FLOOR', 'CHANGEPOINT_PRIOR_SCALE', 'COUNTRY_HOLIDAYS', 
              'HOLIDAYS_PRIOR_SCALE', 'FOURIER_ORDER', 'SEASONALITY_PRIOR_SCALE', 
              'SEASONALITY_MODE', 'INTERVAL_WIDTH']

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
    # Search for model with Cartisan Product of hyperparameters
    parameter_lists = []
    
    for parameter in PARAMETERS:
        parameter_lists.append(getattr(model_config, parameter))
    search_space = product(*parameter_lists)
    # Tune forecast horizon of the chosen model
    payload_list = create_event(search_space)

    max_metric = float('inf')
    chosen_model = None

    # for payload in payload_list:
    #     metric, curr_model = grid_search_worker(payload)
    #     if metric < max_metric:
    #         chosen_model = curr_model
    

    job = group(invoke_lambda.s(
                    function_name = LAMBDA_NAME,
                    sync = True,
                    payload = payload
                    ) for payload in payload_list)
    print("===Async Tasks start===")
    result = job.apply_async()
    result.join()
    model_list = result.get()
    print("===Async Tasks end===")
    import pdb; pdb.set_trace();
    for item in model_list:
        if item[0] < max_metric:
            chosen_model = item[1]
    
    if chosen_model is not None:
        future = chosen_model.make_future_dataframe(periods=int(FORECAST))
        forecast = chosen_model.predict(future)
        time_series = chosen_model.plot(forecast)
        components = chosen_model.plot_component(forecast)
        time_series.savefig('./time_series.png')
        components.savefig('./components.png')

if __name__ == "__main__":
    grid_search_controller()