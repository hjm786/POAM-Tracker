from flask import Blueprint, render_template, request, send_file, jsonify
from models import POAM, Finding, db
from backend.integrations.config_db import get_integration_config, set_integration_config


from backend.findings.poam_manager import (
    export_poam_with_template,
    generate_scan_results_excel,
    get_configuration_findings,
    get_poam_items,
    get_assets_for_poam,
    link_asset_to_poam
)

# Create a Flask Blueprint for routing
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def dashboard():
    """Main dashboard view"""
    return render_template('dashboard.html')

@main_bp.route('/scans')
def get_scans():
    """Return available security scans for dropdown selection"""
    # TODO: Replace with actual scan data from database
    scans = [
        {"id": 1, "name": "AWS Inspector - Critical"},
        {"id": 2, "name": "Tenable - Configuration"}
    ]
    return render_template('fragments/scan_dropdown.html', scans=scans)

@main_bp.route('/scan-results', methods=['GET'])
def get_scan_results():
    """
    Fetch and paginate scan results
    Parameters:
        scan (int): Scan ID from query parameters
        page (int): Current page number, defaults to 1
    """
    scan_id = request.args.get('scan', type=int)
    page = request.args.get('page', default=1, type=int)
    page_size = 5

    # Mock data for demonstration - replace with actual database queries
    all_results = [
        {"tool": "AWS Inspector", "severity": "High", "description": f"Critical vulnerability {i}", "detection_date": "2024-12-01"}
        for i in range(1, 21)  # Simulate 20 results
    ]

    # Implement pagination logic
    total_results = len(all_results)
    start = (page - 1) * page_size
    end = start + page_size
    paginated_results = all_results[start:end]

    total_pages = (total_results + page_size - 1) // page_size
    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_pages else None

    return render_template(
        'fragments/scan_table.html',
        results=paginated_results,
        prev_page=prev_page,
        next_page=next_page
    )



@main_bp.route('/integrations', methods=['GET'])
def integrations():
    """
    Render the integrations management page.
    Returns a list of supported integrations with their current configurations.
    """
    integrations = [
        {"name": "AWS Inspector", "config": get_integration_config("aws_inspector")},
        {"name": "Tenable", "config": get_integration_config("tenable")},
        {"name": "GitHub", "config": get_integration_config("github")},
        {"name": "Google Space", "config": get_integration_config("google_space")},
    ]
    return render_template('integrations.html', integrations=integrations)

@main_bp.route('/integrations/<integration_name>/config-template', methods=['GET'])
def get_config_template(integration_name):
    """
    Return the configuration template for the selected integration.
    
    Provides field definitions for each supported integration including:
    - Field names
    - Labels
    - Input types
    - Available options for select fields
    """
    config_templates = {
        "aws_inspector": {
            "fields": [
                {"name": "access_key", "label": "Access Key", "type": "text"},
                {"name": "secret_key", "label": "Secret Key", "type": "text"},
                {"name": "region", "label": "Region", "type": "text"}
            ]
        },
        "tenable": {
            "fields": [
                {"name": "access_key", "label": "Access Key", "type": "text"},
                {"name": "secret_key", "label": "Secret Key", "type": "text"},
                {"name": "domain", "label": "Domain", "type": "select", "options": ["federal.tenable.com", "cloud.tenable.com"]},
                {"name": "scanner_type", "label": "Scanner Type", "type": "select", "options": ["vulnerability", "compliance"]}
            ]
        },
        "github": {
            "fields": [
                {"name": "access_token", "label": "Access Token", "type": "text"},
                {"name": "repository", "label": "Repository", "type": "text"}
            ]
        },
        "google_space": {
            "fields": [
                {"name": "webhook_url", "label": "Webhook URL", "type": "url"}
            ]
        }
    }

    return jsonify(config_templates.get(integration_name, {"fields": []}))
