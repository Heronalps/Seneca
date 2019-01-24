import sys, os
sys.path.insert(0, './')
sys.path.insert(0, '../')

from helpers.parsers import parse_path
seneca_path = parse_path(os.getcwd(), "Seneca")

from execs import run_prophet
from payloads import payloads as pl
from src.allocated_memory.optimizer import Optimizer
import click, subprocess

@click.command()
@click.option('--config_path', '-c', required=True,
                                     #prompt='Path to hyperparameter config file',
                                     help='Path to hyperparameter config file',
                                     default='./config/multi_regression/config.py')
@click.option('--lambda_path', '-l', required=True,
                                     #prompt='Path to hyperparameter config file',
                                     help='Path to lambda handler',
                                     default='./src/lambda_func/multi_regression/multi_regression.py')
@click.option('--model', '-m', required=True, 
                               #prompt='Specified model',
                               help='The specified model',
                               type = click.Choice(['prophet',
                                             'xgboost',
                                             'multi_regression',
                                             'centaurus',
                                             'random_forest',
                                             'neural_network']))
@click.option('--rebuild', '-b', is_flag=True, default=False, 
                                 help='The lambda package will be rebuilt if true')
@click.option('--optimize', '-o', is_flag=True, default=False,
                                  help="The allocated memory will be optimized if true")

def main(config_path, lambda_path, model, rebuild, optimize):
    click.echo("=============Seneca==============")
    click.echo('The specified model is {0}'.format(model))
    click.echo('Config Path is at {0}'.format(config_path))
    click.echo('Lambda Path is at {0}'.format(lambda_path))
    
    # Rename lambda handler and move to corresponding folder /src/lambda_func/

    commands = "mv {0} {1}; mv {1} {2};".format(lambda_path, 
                                                model + '.py',
                                                seneca_path + '/src/lambda_func/' + model)
    
    p = subprocess.Popen(commands, shell=True)
    p.wait()

    # Both optimization or rebuild need deployment
    if optimize or rebuild:
            auto_deploy(model)
            if optimize:
                auto_optimize(model)

    if model == 'prophet':
        prophet(config_path, run_prophet)

    elif model == 'multi_regression':
        pass
        # multi_regression(config_path, run_multi_regression)


def auto_deploy(model):
    my_env = os.environ.copy()
    p = subprocess.Popen(['docker-compose', "up", "--build"], 
                          env = my_env, 
                          cwd = seneca_path + "/docker/" + model)
    p.wait()

def auto_optimize(model):
    payload = getattr(getattr(pl, model), 'payload')
    optimizer = Optimizer(fn_name=model + '_worker', payload=payload)
    click.echo(optimizer.run())

def prophet(config_path, run_prophet):
    click.echo("Run Hyperparameter Tuning on Prophet")
    click.echo(run_prophet.grid_search_controller(config_path))

def multi_regression(config_path, run_multi_regression):
    pass
