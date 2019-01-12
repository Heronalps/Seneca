# The function (run on EC2 instance) creates celery tasks and retrieve result

from config import model_config, cross_validation_config
import itertools
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

PARAMETERS = ['GROWTH', 'CAP', 'FLOOR', 'CHANGEPOINT_PRIOR_SCALE', 'COUNTRY_HOLIDAYS', 
              'HOLIDAYS_PRIOR_SCALE', 'FOURIER_ORDER', 'SEASONALITY_PRIOR_SCALE', 
              'SEASONALITY_MODE', 'INTERVAL_WIDTH']

def grid_search_controller():
    # Search for model with Cartisan Product of hyperparameters
    parameter_lists = []
    
    for parameter in PARAMETERS:
        parameter_lists.append(getattr(model_config, parameter))
        print ("=====Value List=====")
        print (parameter_lists)
    search_space = itertools.product(*parameter_lists)
    # Tune forecast horizon of the chosen model
    
    
if __name__ == "__main__":
    grid_search_controller()