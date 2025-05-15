import os
import click
from kubernetes import config, client

DEFAULT_KUBECONFIG_PATH = os.path.expanduser("~/.kube/config")

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
@click.option(
    '--kubeconfig',
    default=DEFAULT_KUBECONFIG_PATH,
    show_default=True,
    help='Path to kubeconfig file.'
)
def setup_k8s_connection(kubeconfig):
    """Connect to the Kubernetes cluster and verify the connection."""
    if connect_to_cluster(kubeconfig):
        print("You're now connected. Proceed with further operations.")
    else:
        print("Unable to connect. Check your kubeconfig.")
