from fbprophet import Prophet
import pandas as pd
import boto3, os
from fbprophet.diagnostics import cross_validation
from fbprophet.diagnostics import performance_metrics

local_repo = os.path.join(os.path.sep, "tmp", os.path.basename('csv'))
client = boto3.client('s3')

def read_csv_s3(file_name):
    if not os.path.exists(local_repo):
        os.makedirs(local_repo)
    path = local_repo + '/' + file_name
    bucket = 'prophet-racelab'
    client.download_file(bucket, file_name, path)
    df = pd.read_csv(path)
    return df

# This function trains the time series model based on hyperparameters and dataset.
'''
Parameters:
    event, context
Returns:
    average metric of cross validation performance 
'''
def grid_search_worker(event, context={}):
    # Time series model settings
    
    growth = event['growth'] 
    cap = event['cap'] 
    floor = event['floor'] 
    changepoint_prior_scale = event['changepoint_prior_scale'] 
    country_holidays = event['country_holidays'] 
    holidays_prior_scale = event['holidays_prior_scale'] 
    fourier_order= event['fourier_order'] 
    seasonality_prior_scale = event['seasonality_prior_scale'] 
    seasonality_mode = event['seasonality_mode'] 
    interval_width = event['interval_width'] 
    
    # Cross validation settings
    
    initial = event['initial']
    period = event['period']
    horizon = event['horizon']
    metric = event['metric']

    # Read the dataset from S3 bucket
    df = read_csv_s3('example_wp_log_peyton_manning.csv')    
    # df = pd.read_csv("./example_wp_log_peyton_manning.csv")
    
    # Fit the model
    df['cap'] = cap
    df['floor'] = floor
    model = Prophet(growth = growth, 
                    changepoint_prior_scale = changepoint_prior_scale,
                    holidays_prior_scale = holidays_prior_scale,
                    seasonality_mode = seasonality_mode,
                    interval_width = interval_width)

    model.add_seasonality(name = 'yearly', 
                          period=365, 
                          fourier_order=fourier_order, 
                          prior_scale=seasonality_prior_scale)
    model.add_country_holidays(country_name = country_holidays)

    model.fit(df)
    
    # Cross validation the model

    average_metric = cross_validation_worker(model, initial, period, horizon, metric)
    return (average_metric, model)

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
    df_cv = cross_validation(model, initial = initial, period = period, horizon = horizon)
    df_p = performance_metrics(df_cv)
    average_metric = df_p[metric].mean()
    return average_metric