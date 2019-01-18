import sys, os
sys.path.insert(0, './')
sys.path.insert(0, '../')

from helpers.parsers import parse_path
seneca_path = parse_path(os.getcwd(), "Seneca")

from execs import run_prophet
import click, subprocess

@click.command()
@click.option('--config_path', '-c', required=True,
                                     #prompt='Path to hyperparameter config file',
                                     help='Path to hyperparameter config file')
@click.option('--model', '-m', required=True, 
                               #prompt='Specified model',
                               help='The specified model',
                               type = click.Choice(['prophet',
                                             'xgboost',
                                             'multi_regression',
                                             'centaurus',
                                             'random_forest',
                                             'neural_network']))

def main(config_path, model):
    click.echo("=============Seneca==============")
    click.echo('The specified model is {0}.'.format(model))
    click.echo('Config Path is {0}.'.format(config_path))
    
    if model == 'prophet':
        auto_deploy(model)
        prophet(config_path)

def auto_deploy(model):
    if model == "prophet":
        deploy_prophet()

def deploy_prophet():
    my_env = os.environ.copy()
    p = subprocess.Popen(['docker-compose', "up", "--build"], 
                          env = my_env, 
                          cwd = seneca_path + "/docker/prophet")
    p.wait()
    
def prophet(config):
    click.echo("Config file is at {0}".format(config))
    click.echo(run_prophet.grid_search_controller(config))
