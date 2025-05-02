# 🚀 k8s-infra-automation

A Python-based CLI tool designed to automate Kubernetes infrastructure tasks such as deploying applications, performing health checks, and managing manifests.:contentReference[oaicite:2]{index=2}

---

## 📦 Features

- **Automated Deployments**: :contentReference[oaicite:4]{index=4}
- **Health Monitoring**: :contentReference[oaicite:7]{index=7}
- **Manifest Management**: :contentReference[oaicite:10]{index=10}:contentReference[oaicite:12]{index=12}

---

## 🛠️ Prerequisites

- Python 3.6 or higher

- kubectl configured for your cluster

- Click library for CLI interactions

---

## 📁 Project Structure

```
k8s-infra-automation/
├── cli.py
├── commands/
│   ├── deploy.py
│   └── health.py
├── manifest/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── scaledobject.yaml
├── utils/
│   └── manifest_generator.py
├── requirements.txt
└── README.md
```

- `cli.py`: :Main entry point for the CLI tool.
- `commands/`: :Contains command modules for deployment and health checks.
- `manifest/`: :Holds YAML files for Kubernetes resources
- `utils/`: : Includes helper functions for manifest generation.

---

## 🚀 Getting Started

### 🔧 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Gautamram123/k8s-infra-automation.git
   cd k8s-infra-automation
   ```

2. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

---

## ⚙️ Usage

### Connect to the Kubernetes Cluster:

```bash
python cli.py setup_k8s_connection
```

### Install KEDA:

```bash
python cli.py install_keda
```

### 📦 Create Deployment:

```bash
python cli.py create_deployment
```


### 🩺 Health Check

```bash
python cli.py health_check
```

---

## 📄 Manifest Files

The manifest/ directory contains YAML files for:

- `deployment.yaml`: Defines the deployment configuration.
- `service.yaml`: Exposes the deployment as a service.
- `scaledobject.yaml`: (Optional) Configures KEDA for autoscaling.

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.
---

---
