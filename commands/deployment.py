import click
import subprocess
import os
import tempfile
import yaml

# Define the default path for the manifest file
DEFAULT_MANIFEST_PATH = os.path.join(os.path.dirname(__file__), '..', 'manifest', 'deployment.yaml')

@click.command()
@click.option('--manifest', default=DEFAULT_MANIFEST_PATH, help='Path to the deployment manifest YAML file.')
def create_deployment(manifest):
    """Create a deployment using kubectl and a generated YAML file."""
    try:
        # Check if the file exists
        if not os.path.exists(manifest):
            print(f"❌ The manifest file at {manifest} does not exist. Please check the path.")
            return

        # Load the YAML manifest
        with open(manifest, 'r') as file:
            deployment_manifest = yaml.safe_load(file)

        # Validate the manifest (simple check for apiVersion and kind)
        if deployment_manifest.get('apiVersion') != 'apps/v1' or deployment_manifest.get('kind') != 'Deployment':
            print("❌ Invalid manifest: This is not a valid Kubernetes Deployment manifest.")
            return

        # Use tempfile to generate a temporary file with the manifest
        with tempfile.NamedTemporaryFile('w', suffix='.yaml', delete=False) as f:
            yaml.dump(deployment_manifest, f)
            f.flush()
            subprocess.run(['kubectl', 'apply', '-f', f.name], check=True)
            print(f"✅ Deployment '{deployment_manifest['metadata']['name']}' created successfully using kubectl.")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create deployment: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
