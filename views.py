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

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/scans')
def get_scans():
    scans = [
        {"id": 1, "name": "AWS Inspector - Critical"},
        {"id": 2, "name": "Tenable - Configuration"}
    ]
    return render_template('fragments/scan_dropdown.html', scans=scans)

@main_bp.route('/scan-results', methods=['GET'])
def get_scan_results():
    scan_id = request.args.get('scan', type=int)
    page = request.args.get('page', default=1, type=int)
    page_size = 5

    # Mocked data; replace with actual database queries
    all_results = [
        {"tool": "AWS Inspector", "severity": "High", "description": f"Critical vulnerability {i}", "detection_date": "2024-12-01"}
        for i in range(1, 21)  # Simulate 20 results
    ]

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

@main_bp.route('/poam-items', methods=['GET'])
def poam_items():
    poam_items = get_poam_items()
    return render_template('fragments/poam_table.html', items=poam_items)

@main_bp.route('/export-poam', methods=['GET'])
def export_poam():
    file_path = export_poam_with_template()
    return send_file(file_path, as_attachment=True)

@main_bp.route('/export-scan-results', methods=['GET'])
def export_scan_results():
    scan_id = request.args.get('scan_id')
    file_path = generate_scan_results_excel(scan_id)
    return send_file(file_path, as_attachment=True)

@main_bp.route('/config-findings', methods=['GET'])
def config_findings():
    findings = get_configuration_findings()
    return render_template('fragments/poam-config-table.html', findings=findings)

@main_bp.route('/poam/<int:poam_id>/assets', methods=['GET'])
def poam_assets(poam_id):
    assets = get_assets_for_poam(poam_id)
    return jsonify([{"id": asset.id, "name": asset.name, "description": asset.description} for asset in assets])

@main_bp.route('/poam/<int:poam_id>/link-asset', methods=['POST'])
def link_asset(poam_id):
    asset_data = request.json
    asset = link_asset_to_poam(poam_id, asset_data)
    if asset:
        return jsonify({"message": "Asset linked successfully", "asset_id": asset.id}), 200
    return jsonify({"message": "POA&M item not found"}), 404

@main_bp.route('/integrations', methods=['GET'])
def integrations():
    """
    Render the integrations management page.
    """
    integrations = [
        {"name": "AWS Inspector", "config": get_integration_config("aws_inspector")},
        {"name": "Tenable", "config": get_integration_config("tenable")},
        {"name": "GitHub", "config": get_integration_config("github")},
        {"name": "Google Space", "config": get_integration_config("google_space")},
    ]
    return render_template('integrations.html', integrations=integrations)


@main_bp.route('/integrations/<integration_name>', methods=['POST'])
def update_integration(integration_name):
    """
    Update or save configuration for a specific integration.
    """
    config_data = request.json
    set_integration_config(integration_name, config_data)
    return jsonify({"message": f"{integration_name} configuration updated successfully!"}), 200
