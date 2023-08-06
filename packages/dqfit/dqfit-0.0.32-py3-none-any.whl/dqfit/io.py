from typing import List
import json
from glob import glob
from tqdm import tqdm
import gzip
from pathlib import Path

PACKAGE_BASE = Path(__file__).parent

def read_fhir(dir: str = 'path/to/fhir') -> List[dict]:
    """Return a list of FHIR resources (as JSON) from a directory"""
    bulk_paths = glob(f"{dir}/*.ndjson")
    bundle_paths = glob(f"{dir}/*.json")
    bundle_gz_paths = glob(f"{dir}/*.json.gz")
    fhir_resources = []

    for bulk_path in bulk_paths:
        with open(bulk_path, 'r') as f:
            for line in f:
                fhir_resources.append(json.loads(line))

    for bundle_path in bundle_paths:
        with open(bundle_path, 'r') as f:
            bundle = json.load(f)
            for resource in bundle['entry']:
                fhir_resources.append(resource['resource'])

    for bundle_gz_path in bundle_gz_paths:
        with gzip.open(bundle_gz_path, 'rb') as f:
            bundle = json.load(f)
            for resource in bundle['entry']:
                fhir_resources.append(resource['resource'])

    return fhir_resources
    

def load_context(context_key: str = 'COLE') -> dict:
    context_path = f"{PACKAGE_BASE}/data/context/{context_key}.json"
    with open(context_path, "r") as f:
        context = json.load(f)
    return context
