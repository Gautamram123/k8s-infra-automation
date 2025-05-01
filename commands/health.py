import click
import subprocess

def get_deployment_status(deployment_name):
    """Retrieve deployment status using kubectl."""
    try:
        # Get deployment status
        result = subprocess.run(
            ['kubectl', 'get', 'deployment', deployment_name, '-o', 'json'],
            capture_output=True, text=True, check=True
        )
        deployment_status = result.stdout
        return deployment_status
    except subprocess.CalledProcessError as e:
        print(f"❌ Error retrieving deployment status: {e.stderr}")
        return None


def get_pod_status(deployment_name):
    """Retrieve pod status associated with the deployment using kubectl."""
    try:
        # Get pod status
        result = subprocess.run(
            ['kubectl', 'get', 'pods', '-l', f'app={deployment_name}', '-o', 'json'],
            capture_output=True, text=True, check=True
        )
        pods_status = result.stdout
        return pods_status
    except subprocess.CalledProcessError as e:
        print(f"❌ Error retrieving pod status: {e.stderr}")
        return None


def get_pod_metrics(deployment_name):
    """Retrieve CPU and memory usage metrics for the pods in the deployment."""
    try:
        # Get pod resource usage metrics
        result = subprocess.run(
            ['kubectl', 'top', 'pod', '-l', f'app={deployment_name}', '--no-headers'],
            capture_output=True, text=True, check=True
        )
        pod_metrics = result.stdout
        return pod_metrics
    except subprocess.CalledProcessError as e:
        print(f"❌ Error retrieving pod metrics: {e.stderr}")
        return None


@click.command()
@click.option('--name', prompt='Enter the deployment name to check health', help='Name of the deployment')
def health_check(name):
    """Check the health of the given deployment."""
    print(f"🔍 Checking health for deployment: {name}")
    
    # Retrieve deployment and pod status
    deployment_status = get_deployment_status(name)
    if not deployment_status:
        print(f"❌ Failed to retrieve deployment status for {name}.")
        return

    pods_status = get_pod_status(name)
    if not pods_status:
        print(f"❌ Failed to retrieve pods status for {name}.")
        return

    # Print deployment status
    print("✅ Deployment Status:")
    print(deployment_status)

    # Print pod status
    print("✅ Pod Status:")
    print(pods_status)

    # Retrieve pod metrics (CPU & Memory usage)
    pod_metrics = get_pod_metrics(name)
    if pod_metrics:
        print("✅ Pod Metrics:")
        print(pod_metrics)
    else:
        print("❌ Could not retrieve pod metrics.")

    # Check if any issues or failures exist in the deployment or pods
    if 'replicas' in deployment_status and 'availableReplicas' in deployment_status:
        available_replicas = deployment_status['availableReplicas']
        total_replicas = deployment_status['replicas']
        if available_replicas != total_replicas:
            print(f"⚠️ Warning: Deployment has {total_replicas - available_replicas} unavailable replicas!")
        else:
            print("✅ All replicas are available.")
    else:
        print("❌ Failed to retrieve replica status.")

    # Check pod restarts
    if 'status' in pods_status:
        for pod in pods_status['items']:
            restarts = pod['status']['containerStatuses'][0].get('restartCount', 0)
            if restarts > 0:
                print(f"⚠️ Pod {pod['metadata']['name']} has {restarts} restarts.")
            else:
                print(f"✅ Pod {pod['metadata']['name']} is healthy.")

