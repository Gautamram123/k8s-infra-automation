import subprocess
import sys
import click

def check_helm_installed():
    """Check if Helm is installed."""
    result = subprocess.run(['helm', 'version'], capture_output=True, text=True)
    if result.returncode != 0:
        return False
    return True

def install_helm():
    """Install Helm if not installed."""
    try:
        print("Helm is not installed. Installing Helm...")

        # Here, we can add installation commands based on the platform (e.g., for Linux)
        # For Linux, you could use the following (modify accordingly for other OS):

        subprocess.run(['curl', 'https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash'], check=True)

        print("✅ Helm installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing Helm: {e}")
        sys.exit(1)

@click.command()
def install_keda():
    """Install KEDA in the Kubernetes cluster."""
    # Check if Helm is installed
    if not check_helm_installed():
        user_response = click.prompt(
            "Helm is not installed. Would you like the script to install it for you? (yes/no)",
            type=str,
            default="no"
        ).lower()

        if user_response in ['yes', 'y']:
            install_helm()
        else:
            print("❌ Helm must be installed to proceed with KEDA installation.")
            sys.exit(1)

    try:
        print("✅ Helm is installed. Installing KEDA...")

        # Add KEDA Helm repo
        subprocess.run(['helm', 'repo', 'add', 'kedacore', 'https://kedacore.github.io/charts'], check=True)
        subprocess.run(['helm', 'repo', 'update'], check=True)

        # Create namespace and install KEDA
        subprocess.run(['kubectl', 'create', 'namespace', 'keda'], check=False)
        subprocess.run([
            'helm', 'install', 'keda', 'kedacore/keda',
            '--namespace', 'keda'
        ], check=True)

        print("⏳ Waiting for KEDA operator to be ready...")
        subprocess.run([
            'kubectl', 'rollout', 'status', 'deployment/keda-operator',
            '--namespace', 'keda', '--timeout=60s'
        ], check=True)

        print("✅ KEDA successfully installed and running.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing KEDA: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
