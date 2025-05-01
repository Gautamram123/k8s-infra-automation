import yaml
from pathlib import Path

MANIFEST_DIR = Path(__file__).resolve().parent.parent / "manifest"

def load_manifest(filename):
    with open(MANIFEST_DIR / filename, 'r') as f:
        return yaml.safe_load(f)
