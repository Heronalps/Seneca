#All the lists of hyperparameter of model
GROWTH = ['logistic', 'linear'] # List of string ("logistic", "linear")
CAP = [10, 100] # List of integer / float 
FLOOR = [1, 5] # List of integer / float

CHANGEPOINT_PRIOR_SCALE = [0.05] # List of float within (0, 1) Default = 0.05

'''
Brazil (BR), Indonesia (ID), India (IN), Malaysia (MY), Vietnam (VN), Thailand (TH), Philippines (PH), 
Turkey (TU), Pakistan (PK), Bangladesh (BD), Egypt (EG), China (CN), and Russian (RU)
'''
COUNTRY_HOLIDAYS = ['US'] # List of countries
HOLIDAYS_PRIOR_SCALE = [5.0] # List of float within (0, 10) Default = 10 

FOURIER_ORDER = [10, 20] # List of the fourier order of yearly seasonality
SEASONALITY_PRIOR_SCALE = [0.05] # List of float within (0, 1) Default = 0.5

SEASONALITY_MODE = ['additive', 'multiplicative'] # List of ['additive', 'multiplicative']

INTERVAL_WIDTH = [0.2, 0.9] # List of float within (0, 1) Default = 0.8