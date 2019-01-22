import json

class Prophet:
    payload = json.dumps({'parameters': ['cap', 'changepoint_prior_scale', 'country_holidays', 'floor', 'fourier_order','growth', 'holidays', 'holidays_prior_scale', 'interval_width', 'left_bound', 'right_bound', 'seasonality_mode', 'seasonality_prior_scale', 'dataset', 'forecast', 'horizon', 'initial', 'lambda_name', 'metric', 'period'], 'data': {'cap': 100, 'changepoint_prior_scale': 0.05, 'country_holidays': 'US', 'floor': 10, 'fourier_order': 10, 'growth': 'logistic', 'holidays': '{"holiday": "superbowl", "ds": ["2010-02-07", "2014-02-02", "2016-02-07"], "lower_window": 0, "upper_window":1}', 'holidays_prior_scale': 10, 'interval_width': 0.8, 'left_bound': '2007-12-10', 'right_bound': '2016-01-20', 'seasonality_mode': 'additive', 'seasonality_prior_scale': 0.5, 'dataset': 'example_wp_log_peyton_manning.csv', 'forecast': '360', 'horizon': '365 days', 'initial': '2190 days', 'lambda_name': 'prophet_worker', 'metric': 'mse', 'period': '180 days'}, 'forecast': 0})

class multi_regression:
    payload = json.dumps({"variable_files": "[\"pizero_02.csv\",\"pizero_02_2.csv\",\"pizero_04.csv\", \"pizero_05.csv\", \"pizero_06.csv\"]","target_file": "pizero_02_dht.csv"})