import click
import subprocess
import json


def get_deployment_status(name):
    """Retrieve deployment status and available replicas using kubectl."""
    try:
        # Run kubectl to get the deployment status in JSON format
        result = subprocess.run(
            ['kubectl', 'get', 'deployment', name, '-o', 'json'],
            capture_output=True, text=True, check=True
        )
        # Parse the JSON output
        deployment = json.loads(result.stdout)
        if 'status' in deployment:
            # Extract replicas and availableReplicas
            replicas = deployment['status'].get('replicas', 'N/A')
            available_replicas = deployment['status'].get('availableReplicas', 'N/A')
            return replicas, available_replicas
        else:
            print("⚠️ Deployment status not found.")
            return None
    except subprocess.CalledProcessError as e:
        print(f"❌ Error retrieving deployment status: {e.stderr}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Error decoding JSON response: {e}")
        return None


def get_pod_metrics(name):
    """Retrieve CPU and memory usage metrics for pods using kubectl."""
    try:
        result = subprocess.run(
            ['kubectl', 'top', 'pods', '-l', f'app={name}', '--no-headers'],
            capture_output=True, text=True, check=True
        )
        if result.stdout.strip():
            return result.stdout.strip()  # Return metrics
        else:
            print("⚠️ No pod metrics found.")
            return None
    except subprocess.CalledProcessError as e:
        print(f"❌ Error retrieving pod metrics: {e.stderr}")
        return None


@click.command()
@click.option('--name', prompt='Enter the deployment name to check health', help='Name of the deployment')
def health_check(name):
    """Check the health of the given deployment using kubectl."""
    try:
        print(f"🔍 Checking health for deployment: {name}")

        # Get deployment status
        deployment_status = get_deployment_status(name)
        if not deployment_status:
            return

        replicas, available_replicas = deployment_status
        print(f"Deployment {name} - Replicas: {replicas}, Available Replicas: {available_replicas}")

        # Get pod metrics (if Metrics Server is available)
        metrics = get_pod_metrics(name)
        if metrics:
            print(f"Pod metrics for {name}:\n{metrics}")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")


@click.group()
def cli():
    """Kubernetes CLI Tool for interacting with your cluster."""
    pass


cli.add_command(health_check)

if __name__ == "__main__":
    cli()
