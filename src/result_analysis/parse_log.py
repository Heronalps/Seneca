import os, sys, csv, re, importlib, json, ast
import pandas as pd
from itertools import product
sys.path.insert(0, "./")
from helpers.parsers import split_path
from helpers.parsers import parse_score
from helpers.parsers import parse_metrics

'''
This function queries dataframe with a dictionary with columns' value
'''
def query_df(df, value_dict):
    for key, value in value_dict.items():
        if key in df.columns:
            
            # Core codeline: Filter the df with values in the dict one by one
            df = df.loc[df[key] == value]

    return df.index.tolist()

'''
This function removes columns that have same values in all rows.
'''
def remove_column_same_value(df):
    unique_count = df.apply(pd.Series.nunique)
    df = df.drop(unique_count[unique_count == 1].index, axis = 1)
    return df

'''
This function parses score from log.
metric_pattern = ['Metric mse', 'Accuracy Score']

'''

def parse_log_score(model, folder_path, metric_pattern):
    df = pd.read_csv('../results/spreadsheets/parameter_mapping_{0}.csv'.format(model))
    file_names = os.listdir(folder_path)
    count = 1

    # Remove columns that have all same values
    df = remove_column_same_value(df)

    for file_name in file_names:
        with open(folder_path + file_name, "r") as f:
            line = f.readline()
            indices = []
            while line:
                if line.startswith('{'):
                    parameter_dict = ast.literal_eval(line)

                    # query the df with all values in dict
                    indices = query_df(df, parameter_dict)

                elif line.startswith(metric_pattern) and indices:
                    score = parse_score(line, pattern = metric_pattern)
                    for index in indices:
                        df.loc[index, str(count)] = score

                line = f.readline()

        count = count + 1
        # import pdb; pdb.set_trace();       
    df.to_csv("../results/spreadsheets/{0}_{1}.csv".format(model, metric_pattern), index = False)

'''
This function parses metrics from log.
metric_pattern = ['Duration','Billed Duration','Memory Size', 'Max Memory Used']
'''

def parse_log_metric(model, folder_path, metric_pattern):
    df = pd.read_csv('../results/spreadsheets/parameter_mapping_{0}.csv'.format(model))
    file_names = os.listdir(folder_path)
    count = 1

    # Remove columns that have all same values
    df = remove_column_same_value(df)

    for file_name in file_names:
        with open(folder_path + file_name, "r") as f:
            line = f.readline()
            indices = []
            while line:
                if line.startswith('{'):
                    parameter_dict = ast.literal_eval(line)

                    # query the df with all values in dict
                    indices = query_df(df, parameter_dict)

                elif line.startswith('REPORT') and indices:
                    metrics = parse_metrics(line)
                    for index in indices:
                        df.loc[index, str(count)] = metrics[metric_pattern]

                line = f.readline()

        count = count + 1
        # import pdb; pdb.set_trace();       
    df.to_csv("../results/spreadsheets/{0}_{1}.csv".format(model, metric_pattern), index = False)

'''
This function parses execution time from nohup.out.
'''

def parse_log_execution_time(model, file_path):
    count = 1
    with open(file_path, "r") as f:
        line = f.readline()
        execution_times = {}
        while line:
            if line.startswith('===Async Tasks end==='):
                temp = f.readline()
                execution_times[count] = float(temp)
                count = count + 1
            line = f.readline()
            
    with open("./results/spreadsheets/{0}_execution_times.csv".format(model), "w") as f:
        w = csv.DictWriter(f, execution_times.keys())
        w.writeheader()
        w.writerow(execution_times)



if __name__ == "__main__":
    model = 'prophet'
    folder_path = './cloudwatch/Prophet/'
    parse_log_score(model, folder_path, "Metric mse")
    parse_log_metric(model, folder_path, 'Max Memory Used')
    parse_log_execution_time('prophet', './cloudwatch/Prophet/prophet.out')