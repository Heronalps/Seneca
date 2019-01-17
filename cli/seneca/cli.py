import click

@click.command()
@click.option('--as-cowboy', '-c', is_flag=True, help='Path to hyperparameter config file')
@click.option('--as-cowboy', '-c', is_flag=True, help='Greet as a cowboy.')
@click.option('--as-cowboy', '-c', is_flag=True, help='Greet as a cowboy.')
@click.argument('name', default='world', required=False)
def main(name, as_cowboy):
    greet = 'Howdy' if as_cowboy else 'How'
    click.echo('{0}, {1}.'.format(greet, name))
