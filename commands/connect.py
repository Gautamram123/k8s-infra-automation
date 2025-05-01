import click
from kubernetes import config, client

def connect_to_cluster(kubeconfig_path):
    try:
        config.load_kube_config(config_file=kubeconfig_path) if kubeconfig_path else config.load_kube_config()
        client.CoreV1Api().list_node()
        print("✅ Successfully connected to Kubernetes cluster!")
        return True
    except Exception as e:
        print(f"❌ Failed to connect to the cluster: {e}")
        return False

@click.command()
@click.option('--kubeconfig', prompt='Enter the path to your kubeconfig file (or press Enter for default)',
              help='Path to kubeconfig file.')
def setup_k8s_connection(kubeconfig):
    """Connect to the Kubernetes cluster and verify the connection."""
    if connect_to_cluster(kubeconfig):
        print("You're now connected. Proceed with further operations.")
    else:
        print("Unable to connect. Check your kubeconfig.")
