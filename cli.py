import click
from config_parser import parse_config
from deploy import deploy
from rollback import rollback

@click.group()
def cli():
    """DeployMaster CLI tool for simplified deployment configurations."""
    pass

@cli.command(name='deploy')
@click.argument('config_file', type=click.Path(exists=True))
def deploy_command(config_file):
    """Deploy using the specified configuration file."""
    config = parse_config(config_file)
    deploy(config)

@cli.command(name='rollback')
@click.argument('config_file', type=click.Path(exists=True))
def rollback_command(config_file):
    """Rollback using the specified configuration file."""
    config = parse_config(config_file)
    rollback(config)

if __name__ == '__main__':
    cli()