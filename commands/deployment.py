import click
import subprocess
import yaml
import tempfile
import os
from utils.manifest_loader import load_manifest

def update_manifest(manifest, replacements):
    yaml_str = yaml.dump(manifest)
    for key, val in replacements.items():
        yaml_str = yaml_str.replace(f"placeholder", val)
    return yaml.safe_load(yaml_str)

@click.command()
@click.option('--name', prompt='Deployment name', help='Name of the deployment')
@click.option('--image', prompt='Docker image (e.g., nginx:latest)', help='Container image')
@click.option('--cpu', prompt='CPU (e.g., 200m)', help='CPU request/limit')
@click.option('--memory', prompt='Memory (e.g., 256Mi)', help='Memory request/limit')
@click.option('--port', default=80, help='Container port')
@click.option('--min-replicas', default=1, help='Minimum replicas')
@click.option('--max-replicas', default=5, help='Maximum replicas')
@click.option('--keda-trigger', prompt='KEDA trigger type (e.g., kafka)', help='KEDA trigger type')
@click.option('--trigger-metadata', multiple=True, help='Trigger metadata in key=value format')
def create_deployment(name, image, cpu, memory, port, min_replicas, max_replicas, keda_trigger, trigger_metadata):
    try:
        trigger_meta_dict = dict(kv.split('=') for kv in trigger_metadata)
        
        # Load and modify manifests
        deployment = load_manifest("deployment.yaml")
        service = load_manifest("service.yaml")
        scaledobject = load_manifest("scaledobject.yaml")

        deployment = update_manifest(deployment, {
            'placeholder': name,
        })
        deployment['spec']['template']['spec']['containers'][0]['image'] = image
        deployment['spec']['template']['spec']['containers'][0]['ports'][0]['containerPort'] = port
        deployment['spec']['template']['spec']['containers'][0]['resources'] = {
            'requests': {'cpu': cpu, 'memory': memory},
            'limits': {'cpu': cpu, 'memory': memory}
        }

        service = update_manifest(service, {
            'placeholder': name,
        })
        service['spec']['ports'][0]['port'] = port
        service['spec']['ports'][0]['targetPort'] = port

        scaledobject = update_manifest(scaledobject, {
            'placeholder': name,
        })
        scaledobject['spec']['minReplicaCount'] = min_replicas
        scaledobject['spec']['maxReplicaCount'] = max_replicas
        scaledobject['spec']['triggers'] = [{
            'type': keda_trigger,
            'metadata': trigger_meta_dict
        }]

        with tempfile.TemporaryDirectory() as tmpdir:
            def write_and_apply(obj, fname):
                fpath = os.path.join(tmpdir, fname)
                with open(fpath, 'w') as f:
                    yaml.dump(obj, f)
                subprocess.run(['kubectl', 'apply', '-f', fpath], check=True)

            write_and_apply(deployment, 'deployment.yaml')
            write_and_apply(service, 'service.yaml')
            write_and_apply(scaledobject, 'scaledobject.yaml')

        print(f"✅ Deployment '{name}' created with autoscaling!")

    except Exception as e:
        print(f"❌ Failed to create deployment: {e}")
