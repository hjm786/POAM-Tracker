from flask import Blueprint, render_template, request, send_file
from models import db, Integration, POAM, Finding
import pandas as pd
from backend.findings.poam_manager import generate_poam_excel
from backend.findings.scan_manager import generate_scan_results_excel
from flask import render_template
from jinja2 import TemplateNotFound
from backend.findings.poam_manager import get_configuration_findings


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
    # Get the scan ID and pagination parameters
    scan_id = request.args.get('scan', type=int)
    page = request.args.get('page', default=1, type=int)
    page_size = 5

    # Mocked data; replace with actual database queries
    all_results = [
        {"tool": "AWS Inspector", "severity": "High", "description": f"Critical vulnerability {i}", "detection_date": "2024-12-01"}
        for i in range(1, 21)  # Simulate 20 results
    ]

    # Paginate results
    total_results = len(all_results)
    start = (page - 1) * page_size
    end = start + page_size
    paginated_results = all_results[start:end]

    # Calculate pagination
    total_pages = (total_results + page_size - 1) // page_size
    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_pages else None

    return render_template(
        'fragments/scan_table.html',
        results=paginated_results,
        prev_page=prev_page,
        next_page=next_page
    )

@main_bp.route('/poam-items')
def poam_items():
    status = request.args.get('status', 'Active')
    poam_items = POAM.query.filter_by(status=status).all()
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
    """
    Render the Configuration Findings table.
    """
    findings = get_configuration_findings()
    return render_template('fragments/poam-config-table.html', findings=findings)

@main_bp.route('/poam-items', methods=['GET'])
def poam_items():
    poam_items = POAM.query.all()  # Fetch all POA&M items
    return render_template('fragments/poam_table.html', items=poam_items)

