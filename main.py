import click
from helm_utils import install_keda
from k8s_utils import create_deployment_with_keda
from health_check import check_deployment_health

@click.group()
def cli():
    """Kubernetes Infrastructure Automation CLI"""
    pass

@cli.command()
def setup_keda():
    """Install KEDA in the Kubernetes cluster using Helm"""
    install_keda()

@cli.command()
@click.option('--name', required=True, help='Deployment name')
@click.option('--image', required=True, help='Container image')
@click.option('--cpu', default='100m', help='CPU limit')
@click.option('--memory', default='128Mi', help='Memory limit')
@click.option('--port', default=80, help='Container port')
@click.option('--event-type', default='cpu', type=click.Choice(['cpu', 'custom']), help='Scaling trigger')
def create_deployment(name, image, cpu, memory, port, event_type):
    """Create a deployment, service, and KEDA scaler"""
    create_deployment_with_keda(name, image, cpu, memory, port, event_type)

@cli.command()
@click.option('--name', required=True, help='Deployment name to check')
def health(name):
    """Check health of a Kubernetes deployment"""
    check_deployment_health(name)

if __name__ == '__main__':
    cli()
