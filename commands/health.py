import subprocess
import click

def install_metrics_server():
    """Install Kubernetes Metrics Server using kubectl."""
    try:
        print("📦 Installing Metrics Server...")
        subprocess.run([
            "kubectl", "apply", "-f",
            "https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml"
        ], check=True)

        subprocess.run([
            "kubectl", "rollout", "status", "deployment/metrics-server",
            "-n", "kube-system", "--timeout=60s"
        ], check=True)

        print("✅ Metrics Server successfully installed.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Metrics Server: {e}")

@click.command()
@click.option('--name', prompt='Enter the deployment name to check health', help='Name of the deployment')
def health_check(name):
    """Check deployment health, status, and resource usage."""
    try:
        print(f"🔍 Checking deployment and pod status for '{name}'")

        subprocess.run(['kubectl', 'get', 'deployment', name], check=True)

        pods_result = subprocess.run(
            ['kubectl', 'get', 'pods', '-l', f'app={name}',
             '-o', 'custom-columns=NAME:.metadata.name,STATUS:.status.phase',
             '--no-headers'],
            capture_output=True, text=True, check=True
        )
        print("🩺 Pod Status:\n" + pods_result.stdout.strip())

        print("📊 Retrieving pod metrics...")
        metrics_result = subprocess.run(
            ['kubectl', 'top', 'pods', '-l', f'app={name}'],
            capture_output=True, text=True
        )

        if metrics_result.returncode != 0:
            stderr = metrics_result.stderr.strip()
            print(f"⚠️ Error retrieving pod metrics: {stderr}")
            if "Metrics API not available" in stderr:
                if click.confirm("📉 Metrics Server is not installed. Would you like to install it now?"):
                    install_metrics_server()
                    print("🔁 Re-run the health check after installation completes.")
                else:
                    print("❌ Cannot retrieve metrics without Metrics Server.")
            return

        print("📈 Pod Metrics:\n" + metrics_result.stdout.strip())

    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing kubectl: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
