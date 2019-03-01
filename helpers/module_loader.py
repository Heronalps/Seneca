import importlib.util
from helpers.parsers import split_path

def load(config_path):
    _path_prefix, filename = split_path(config_path)
    spec = importlib.util.spec_from_file_location(filename, config_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    return config