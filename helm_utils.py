import subprocess

def install_keda():
    try:
        subprocess.run(["helm", "repo", "add", "kedacore", "https://kedacore.github.io/charts"], check=True)
        subprocess.run(["helm", "repo", "update"], check=True)
        subprocess.run([
            "helm", "install", "keda", "kedacore/keda",
            "--namespace", "keda",
            "--create-namespace"
        ], check=True)
        print("✅ KEDA installed successfully.")
    except subprocess.CalledProcessError as e:
        print("❌ Error during KEDA installation:", e)
