from kubernetes import client, config

def check_deployment_health(name):
    config.load_kube_config()
    core_v1 = client.CoreV1Api()

    try:
        pods = core_v1.list_namespaced_pod(namespace="default", label_selector=f"app={name}").items
        if not pods:
            print(f"⚠️ No pods found for deployment '{name}'.")
            return

        for pod in pods:
            pod_name = pod.metadata.name
            status = pod.status.phase
            restarts = sum(cs.restart_count for cs in pod.status.container_statuses or [])
            print(f"📦 Pod: {pod_name}, Status: {status}, Restarts: {restarts}")
    except Exception as e:
        print("❌ Error during health check:", e)
