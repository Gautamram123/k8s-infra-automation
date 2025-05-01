from kubernetes import client, config
import os

def connect_to_cluster():
    """Connect to the Kubernetes cluster using kubeconfig."""
    kubeconfig_path = os.getenv('KUBECONFIG', os.path.expanduser('~/.kube/config'))
    
    if not os.path.exists(kubeconfig_path):
        print("❌ kubeconfig not found at", kubeconfig_path)
        return None

    try:
        config.load_kube_config(kubeconfig=kubeconfig_path)
        print("✅ Connected to Kubernetes cluster successfully.")
        return client
    except Exception as e:
        print("❌ Error connecting to the cluster:", e)
        return None

def create_deployment_with_keda(name, image, cpu, memory, port, event_type):
    """Create deployment, service, and KEDA scaler."""
    k8s_client = connect_to_cluster()
    if not k8s_client:
        return

    apps_v1 = k8s_client.AppsV1Api()
    core_v1 = k8s_client.CoreV1Api()
    custom_api = k8s_client.CustomObjectsApi()

    # Deployment creation logic
    deployment = client.V1Deployment(
        metadata=client.V1ObjectMeta(name=name),
        spec=client.V1DeploymentSpec(
            replicas=1,
            selector={"matchLabels": {"app": name}},
            template=client.V1PodTemplateSpec(
                metadata={"labels": {"app": name}},
                spec=client.V1PodSpec(
                    containers=[client.V1Container(
                        name=name,
                        image=image,
                        ports=[client.V1ContainerPort(container_port=port)],
                        resources=client.V1ResourceRequirements(
                            limits={"cpu": cpu, "memory": memory},
                            requests={"cpu": cpu, "memory": memory}
                        )
                    )]
                )
            )
        )
    )
    service = client.V1Service(
        metadata=client.V1ObjectMeta(name=name),
        spec=client.V1ServiceSpec(
            selector={"app": name},
            ports=[client.V1ServicePort(port=port, target_port=port)]
        )
    )

    # ScaledObject creation for KEDA
    scaled_object = {
        "apiVersion": "keda.sh/v1alpha1",
        "kind": "ScaledObject",
        "metadata": {"name": f"{name}-scaler", "namespace": "default"},
        "spec": {
            "scaleTargetRef": {"name": name},
            "minReplicaCount": 1,
            "maxReplicaCount": 5,
            "triggers": [{
                "type": event_type,
                "metadata": {
                    "type": "Utilization",
                    "value": "50"
                }
            }] if event_type == "cpu" else []
        }
    }

    try:
        apps_v1.create_namespaced_deployment(namespace="default", body=deployment)
        core_v1.create_namespaced_service(namespace="default", body=service)
        custom_api.create_namespaced_custom_object(
            group="keda.sh",
            version="v1alpha1",
            namespace="default",
            plural="scaledobjects",
            body=scaled_object
        )
        print(f"✅ Deployment '{name}' created with KEDA scaling.")
    except Exception as e:
        print("❌ Error creating deployment or scaler:", e)
