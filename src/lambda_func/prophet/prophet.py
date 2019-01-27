from fbprophet import Prophet
import pandas as pd
import boto3, os, datetime, json
from fbprophet.diagnostics import cross_validation
from fbprophet.diagnostics import performance_metrics

local_repo = os.path.join(os.path.sep, "tmp", os.path.basename('csv'))
client = boto3.client('s3')
s3 = boto3.resource('s3')

def read_csv_s3(file_name):
    if not os.path.exists(local_repo):
        os.makedirs(local_repo)
    path = local_repo + '/' + file_name
    bucket = 'prophet-racelab'
    client.download_file(bucket, file_name, path)
    df = pd.read_csv(path)
    return df

def upload_csv_s3(outfile):
    s3.meta.client.upload_file(
        Filename = outfile,
        Bucket = 'seneca-racelab',
        Key = "prophet_{0}.png".format(str(datetime.datetime.now().time()))
    )

# This function trains the time series model based on hyperparameters and dataset.
'''
Parameters:
    event, context
Returns:
    average metric of cross validation performance 
'''

def grid_search_worker(event, context={}):
    # Time series model settings
    parameter_list = event['parameters']
    parameters = {}
    for key in parameter_list:
        # Special case for holidays, because it is a json string
        if key == 'holidays':
            holidays_dict = json.loads(event['data'][key])
            continue
        parameters[key] = event['data'][key]

    forecast = event['forecast']

    # Read the dataset from S3 bucket
    # df = read_csv_s3(parameters['dataset'])    
    df = pd.read_csv("./datasets/prophet/example_wp_log_peyton_manning.csv")

    # Transfer holiday to data frame
    if holidays_dict is not None:
        parameters['holidays'] = pd.DataFrame({
            'holiday': holidays_dict['holiday'],
            'ds': pd.to_datetime(holidays_dict['ds']),
            'lower_window': holidays_dict['lower_window'],
            'upper_window': holidays_dict['upper_window'],
        })

    # Fit the model
    df['cap'] = parameters['cap']
    df['floor'] = parameters['floor']
    model = Prophet(growth = parameters['growth'], 
                    changepoint_prior_scale = parameters['changepoint_prior_scale'],
                    holidays = parameters['holidays'],
                    holidays_prior_scale = parameters['holidays_prior_scale'],
                    seasonality_mode = parameters['seasonality_mode'],
                    interval_width = parameters['interval_width'])

    model.add_seasonality(name = 'yearly', 
                          period=365, 
                          fourier_order=parameters['fourier_order'], 
                          prior_scale=parameters['seasonality_prior_scale'])
    model.add_country_holidays(country_name = parameters['country_holidays'])

    # Truncate the time series

    df.loc[(df['ds'] <= parameters['left_bound']) & 
           (df['ds'] >= parameters['right_bound']), 'y'] = None

    print ("=====Fit the Model=======")
    model.fit(df)
    
    if forecast == 0:
        # Cross validation the model
        print ("=====Cross Validation=======")
        average_metric = cross_validation_worker(model, 
                                                 parameters['initial'], 
                                                 parameters['period'], 
                                                 parameters['horizon'], 
                                                 parameters['metric'])
        print("======Return average metric and event=======")
        return {'average_metric' : average_metric, 'event' : event}
    
    else:
        future = model.make_future_dataframe(periods=int(forecast))
        forecast = model.predict(future)
        time_series = model.plot(forecast)
        components = model.plot_components(forecast)
        time_series.savefig(local_repo + '/time_series.png')
        upload_csv_s3(local_repo + '/time_series.png')
        components.savefig(local_repo + '/components.png')
        upload_csv_s3(local_repo + '/components.png')
        return "Graphs are uploaded to S3"

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