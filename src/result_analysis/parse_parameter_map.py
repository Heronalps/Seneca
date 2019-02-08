import os, sys, csv, re, importlib.util
from itertools import product
sys.path.insert(0, "./")
print (sys.path)
from helpers.parsers import split_path

def parse_parameter_map(config_path, lambda_name):
    # Dynamic importing config file from config_path
    _path_prefix, filename = split_path(config_path)
    spec = importlib.util.spec_from_file_location(filename, config_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    
    # Dynamic load parameters 
    PARAMETERS = []
    
    for key in dir(config.Hyperparameter):
        if key.isupper():
            PARAMETERS.append(key)

    # Tune forecast horizon of the chosen model
    create_event(config, PARAMETERS, lambda_name)
    sys.path.pop(0)


def create_event(config, PARAMETERS, LAMBDA_NAME):
    # Search for model with Cartisan Product of hyperparameters
    parameter_lists = []
    for parameter in PARAMETERS:
        parameter_lists.append(getattr(config.Hyperparameter, parameter))
    search_space = product(*parameter_lists)
    
    payload_list = []

    for item in search_space:
        payload = {}
        for key, value in zip(PARAMETERS, list(item)):
            payload[key.lower()] = value
        payload_list.append(payload)
    
    with open("./results/spreadsheets/parameter_mapping_" + LAMBDA_NAME + ".csv", "a") as f:

        first_dict = payload_list[0]
        w = csv.DictWriter(f, first_dict.keys())
        w.writeheader()
        for payload in payload_list:
            w.writerow(payload)

if __name__ == "__main__":
    models = ['prophet', 'neural_network', 'svc', 'xgboost']
    for model in models:
        parse_parameter_map("/Users/michaelzhang/Downloads/Seneca/config/{0}/config.py".format(model), model)