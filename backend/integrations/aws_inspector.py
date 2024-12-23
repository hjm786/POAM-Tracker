import boto3
from config_db import get_integration_config

def fetch_aws_inspector_findings():
    """
    Fetch findings from AWS Inspector and normalize the data.
    """
    config = get_integration_config('aws_inspector')
    if not config:
        raise ValueError("AWS Inspector integration is not configured.")

    # Initialize AWS Inspector client
    client = boto3.client(
        'inspector2',
        aws_access_key_id=config['access_key'],
        aws_secret_access_key=config['secret_key'],
        region_name=config['region']
    )

    # Example: Fetch findings
    findings = client.list_findings()
    return normalize_findings(findings['findings'])

def normalize_findings(findings):
    """
    Normalize AWS Inspector findings to match the app's data model.
    """
    normalized = []
    for finding in findings:
        normalized.append({
            'tool': 'AWS Inspector',
            'severity': finding['severity'],
            'description': finding['title'],
            'detection_date': finding['createdAt'].strftime('%Y-%m-%d'),
            'status': 'Active'
        })
    return normalized
