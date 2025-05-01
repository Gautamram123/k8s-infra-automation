import click
from commands.connect import setup_k8s_connection
from commands.install_keda import install_keda
from commands.deployment import create_deployment
from commands.health import health_check

@click.group()
def cli():
    """Kubernetes CLI Tool for interacting with your cluster."""
    pass

cli.add_command(setup_k8s_connection)
cli.add_command(install_keda)
cli.add_command(create_deployment)
cli.add_command(health_check)

if __name__ == "__main__":
    cli()