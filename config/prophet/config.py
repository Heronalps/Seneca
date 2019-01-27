import json
class Hyperparameter:
    #All the lists of hyperparameter of model
    GROWTH = ['logistic', 'linear'] # List of string ("logistic", "linear")
    CAP = [13] # List of integer / float 
    FLOOR = [5] # List of integer / float
    CHANGEPOINT_PRIOR_SCALE = [0.05, 0.5] # List of float within (0, 1) Default = 0.05

    data = {
      'holiday': 'superbowl',
      'ds': ['2010-02-07', '2014-02-02', '2016-02-07'],
      'lower_window': 0,
      'upper_window': 1,
    }
    json_str = json.dumps(data)
    HOLIDAYS = [json_str] # List of the customized holidays 

    '''
    Brazil (BR), Indonesia (ID), India (IN), Malaysia (MY), Vietnam (VN), Thailand (TH), Philippines (PH), 
    Turkey (TU), Pakistan (PK), Bangladesh (BD), Egypt (EG), China (CN), and Russian (RU)
    '''
    COUNTRY_HOLIDAYS = ['US'] # List of countries
    HOLIDAYS_PRIOR_SCALE = [1, 5, 10] # List of float within (0, 10) Default = 10 

    FOURIER_ORDER = [5, 10, 15, 20] # List of the fourier order of yearly seasonality
    SEASONALITY_PRIOR_SCALE = [0.1, 0.5] # List of float within (0, 1) Default = 0.5

    SEASONALITY_MODE = ['additive', 'multiplicative'] # List of ['additive', 'multiplicative']

    INTERVAL_WIDTH = [0.5, 0.8] # List of float within (0, 1) Default = 0.8

    # MCMC_SAMPLES = [10] # List of Full Bayesian Sampling size

    LEFT_BOUND = ['2007-12-10'] # List of left bound of time series
    RIGHT_BOUND = ['2016-01-20'] # list of right bound of time series

class Cross_Validation:
    # Four parameters of cross validation 

    INITIAL = '2190 days'
    PERIOD = '180 days'
    HORIZON = '365 days'

    # Available metrics: mse, rmse, mae, mape, coverage
    # mape is not scale-invariant
    METRIC = 'mse'

    # The Dataset filename 
    DATASET = 'example_wp_log_peyton_manning.csv'

    # Forecast horizon
    FORECAST = '360'

    # Lambda function name
    LAMBDA_NAME = 'prophet_worker'