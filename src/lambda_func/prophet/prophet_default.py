from fbprophet import Prophet
import pandas as pd
import boto3, os, datetime, json
from fbprophet.diagnostics import cross_validation
from fbprophet.diagnostics import performance_metrics

# This function trains the time series model based on hyperparameters and dataset.
'''
Parameters:
    event, context
Returns:
    average metric of cross validation performance 
'''

def grid_search_worker():
  
    df = pd.read_csv("./datasets/prophet/example_wp_log_peyton_manning.csv")

    model = Prophet()

    print ("=====Fit the Model=======")
    model.fit(df)
    
    # Four parameters of cross validation 

    initial = '2190 days'
    period = '180 days'
    horizon = '365 days'

    # Available metrics: mse, rmse, mae, mape, coverage
    # mape is not scale-invariant
    metric = 'mse'

    # Cross validation the model
    print ("=====Cross Validation=======")
    average_metric = cross_validation_worker(model, initial, period, horizon, metric)
    print("======Return average metric and event=======")
    print ('average_metric {0}'.format(average_metric))

# This function (run on Lambda) cross validate the chosen model

'''
    Parameters:
        initial
        period
        horizon
        metric - ['MSE', 'RMSE', 'MAE', 'MAPE', 'COVERAGE']
    Returns:
        Average of metric over performance metrics dataframe
'''

def cross_validation_worker(model, initial, period, horizon, metric):
    df_cv = cross_validation(model, initial = initial, 
                                    period = period, 
                                    horizon = horizon)
    df_p = performance_metrics(df_cv)
    average_metric = df_p[metric].mean()
    return average_metric

if __name__ == "__main__":
    grid_search_worker()