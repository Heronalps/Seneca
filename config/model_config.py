import json

#All the lists of hyperparameter of model
GROWTH = ['logistic', 'linear'] # List of string ("logistic", "linear")
CAP = [100] # List of integer / float 
FLOOR = [10] # List of integer / float
CHANGEPOINT_PRIOR_SCALE = [0.05] # List of float within (0, 1) Default = 0.05

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
HOLIDAYS_PRIOR_SCALE = [10] # List of float within (0, 10) Default = 10 

FOURIER_ORDER = [10, 20] # List of the fourier order of yearly seasonality
SEASONALITY_PRIOR_SCALE = [0.5] # List of float within (0, 1) Default = 0.5

SEASONALITY_MODE = ['additive', 'multiplicative'] # List of ['additive', 'multiplicative']

INTERVAL_WIDTH = [0.8] # List of float within (0, 1) Default = 0.8

# MCMC_SAMPLES = [10] # List of Full Bayesian Sampling size

LEFT_BOUND = ['2007-12-10'] # List of left bound of time series
RIGHT_BOUND = ['2016-01-20'] # list of right bound of time series
