from tenable.io import TenableIO
from config_db import get_integration_config

def fetch_tenable_findings():
    """
    Fetch findings from Tenable and normalize the data.
    """
    config = get_integration_config('tenable')
    if not config:
        raise ValueError("Tenable integration is not configured.")

    # Initialize Tenable client
    tio = TenableIO(config['access_key'], config['secret_key'])

    # Example: Fetch vulnerabilities
    vulnerabilities = tio.vulns.list()
    return normalize_findings(vulnerabilities)

def normalize_findings(vulnerabilities):
    """
    Normalize Tenable findings to match the app's data model.
    """
    normalized = []
    for vuln in vulnerabilities:
        normalized.append({
            'tool': 'Tenable',
            'severity': vuln['severity'],
            'description': vuln['plugin_name'],
            'detection_date': vuln['first_found'],
            'status': 'Active' if vuln['state'] == 'OPEN' else 'Resolved'
        })
    return normalized
