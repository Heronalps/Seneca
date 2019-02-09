import os, sys, csv, re, importlib, json, ast
import pandas as pd
from itertools import product
sys.path.insert(0, "./")
from helpers.parsers import split_path
from helpers.parsers import parse_score

'''
This function queries dataframe with a dictionary with columns' value
'''
def query_df(df, value_dict):
    indices = []
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

def parse_log(model, folder_path, line_pattern, metric_pattern):
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

                elif line.startswith(line_pattern) and indices:
                    mse = parse_score(line, pattern = metric_pattern)
                    for index in indices:
                        df.loc[index, str(count)] = mse

                line = f.readline()

        count = count + 1
        # import pdb; pdb.set_trace();       
    df.to_csv("../results/spreadsheets/{0}.csv".format(model), index = False)


if __name__ == "__main__":
    model = 'prophet'
    folder_path = '../cloudwatch/Prophet/'
    parse_log(model, folder_path, 'Metric', "Metric mse")