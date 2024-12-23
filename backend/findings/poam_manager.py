from openpyxl import load_workbook
from flask import send_file
from datetime import datetime
from models import POAM, Finding, ConfigurationFinding, Asset, db

TEMPLATE_PATH = "/mnt/data/FedRAMP-POAM-Template.xlsx"

def export_poam_with_template():
    workbook = load_workbook(TEMPLATE_PATH)

    open_sheet = workbook["Open POA&M Items"]
    closed_sheet = workbook["Closed POA&M Items"]
    config_sheet = workbook["Configuration Findings"]

    open_items = POAM.query.filter_by(status="Active").all()
    closed_items = POAM.query.filter_by(status="Resolved").all()
    configuration_findings = ConfigurationFinding.query.all()

    # Fetch POA&M items
    open_items = POAM.query.filter_by(status="Active").all()
    closed_items = POAM.query.filter_by(status="Resolved").all()

    # Fetch Configuration Findings
    configuration_findings = ConfigurationFinding.query.all()


   # Populate Open POA&M Items
    open_row = 6
    for item in open_items:
      open_sheet[f"A{open_row}"] = item.id  # POAM ID
      open_sheet[f"B{open_row}"] = item.controls  # Controls
      open_sheet[f"C{open_row}"] = item.weakness_name  # Weakness Name
      open_sheet[f"D{open_row}"] = item.weakness_description  # Weakness Description
      open_sheet[f"E{open_row}"] = item.detector_source  # Weakness Detector Source
      open_sheet[f"F{open_row}"] = item.source_identifier  # Weakness Source Identifier
      open_sheet[f"G{open_row}"] = item.asset_identifier  # Asset Identifier
      open_sheet[f"H{open_row}"] = item.point_of_contact  # Point of Contact
      open_sheet[f"I{open_row}"] = item.resources_required  # Resources Required
      open_sheet[f"J{open_row}"] = item.remediation_plan  # Overall Remediation Plan
      open_sheet[f"K{open_row}"] = datetime.strftime(item.detection_date, "%m/%d/%Y") if item.detection_date else ""  # Original Detection Date
      open_sheet[f"L{open_row}"] = datetime.strftime(item.completion_date, "%m/%d/%Y") if item.completion_date else ""  # Scheduled Completion Date
      open_sheet[f"M{open_row}"] = item.planned_milestones  # Planned Milestones
      open_sheet[f"N{open_row}"] = item.milestone_changes  # Milestone Changes
      open_sheet[f"O{open_row}"] = datetime.strftime(item.status_date, "%m/%d/%Y") if item.status_date else ""  # Status Date
      open_sheet[f"P{open_row}"] = item.vendor_dependency  # Vendor Dependency
      open_sheet[f"Q{open_row}"] = datetime.strftime(item.vendor_checkin_date, "%m/%d/%Y") if item.vendor_checkin_date else ""  # Last Vendor Check-in Date
      open_sheet[f"R{open_row}"] = item.product_name  # Vendor Dependent Product Name
      open_sheet[f"S{open_row}"] = item.original_risk_rating  # Original Risk Rating
      open_sheet[f"T{open_row}"] = item.adjusted_risk_rating  # Adjusted Risk Rating
      open_sheet[f"U{open_row}"] = item.risk_adjustment  # Risk Adjustment
      open_sheet[f"V{open_row}"] = item.false_positive  # False Positive
      open_sheet[f"W{open_row}"] = item.operational_requirement  # Operational Requirement
      open_sheet[f"X{open_row}"] = item.deviation_rationale  # Deviation Rationale
      open_sheet[f"Y{open_row}"] = item.supporting_documents  # Supporting Documents
      open_sheet[f"Z{open_row}"] = item.comments  # Comments
      open_sheet[f"AA{open_row}"] = item.auto_approve  # Auto-Approve
      open_sheet[f"AB{open_row}"] = item.bod_22_01_tracking  # Binding Operational Directive 22-01 tracking
      open_sheet[f"AC{open_row}"] = datetime.strftime(item.bod_22_01_due_date, "%m/%d/%Y") if item.bod_22_01_due_date else ""  # Binding Operational Directive 22-01 Due Date
      open_sheet[f"AD{open_row}"] = item.cve  # CVE
      open_sheet[f"AE{open_row}"] = item.service_name  # Service Name
      open_row += 1

    # Populate Closed POA&M Items
    closed_row = 6
    for item in closed_items:
      closed_sheet[f"A{closed_row}"] = item.id  # POAM ID
      closed_sheet[f"B{closed_row}"] = item.controls  # Controls
      closed_sheet[f"C{closed_row}"] = item.weakness_name  # Weakness Name
      closed_sheet[f"D{closed_row}"] = item.weakness_description  # Weakness Description
      closed_sheet[f"E{closed_row}"] = item.detector_source  # Weakness Detector Source
      closed_sheet[f"F{closed_row}"] = item.source_identifier  # Weakness Source Identifier
      closed_sheet[f"G{closed_row}"] = item.asset_identifier  # Asset Identifier
      closed_sheet[f"H{closed_row}"] = item.point_of_contact  # Point of Contact
      closed_sheet[f"I{closed_row}"] = item.resources_required  # Resources Required
      closed_sheet[f"J{closed_row}"] = item.remediation_plan  # Overall Remediation Plan
      closed_sheet[f"K{closed_row}"] = datetime.strftime(item.detection_date, "%m/%d/%Y") if item.detection_date else ""  # Original Detection Date
      closed_sheet[f"L{closed_row}"] = datetime.strftime(item.completion_date, "%m/%d/%Y") if item.completion_date else ""  # Scheduled Completion Date
      closed_sheet[f"M{closed_row}"] = item.planned_milestones  # Planned Milestones
      closed_sheet[f"N{closed_row}"] = item.milestone_changes  # Milestone Changes
      closed_sheet[f"O{closed_row}"] = datetime.strftime(item.status_date, "%m/%d/%Y") if item.status_date else ""  # Status Date
      closed_sheet[f"P{closed_row}"] = item.vendor_dependency  # Vendor Dependency
      closed_sheet[f"Q{closed_row}"] = datetime.strftime(item.vendor_checkin_date, "%m/%d/%Y") if item.vendor_checkin_date else ""  # Last Vendor Check-in Date
      closed_sheet[f"R{closed_row}"] = item.product_name  # Vendor Dependent Product Name
      closed_sheet[f"S{closed_row}"] = item.original_risk_rating  # Original Risk Rating
      closed_sheet[f"T{closed_row}"] = item.adjusted_risk_rating  # Adjusted Risk Rating
      closed_sheet[f"U{closed_row}"] = item.risk_adjustment  # Risk Adjustment
      closed_sheet[f"V{closed_row}"] = item.false_positive  # False Positive
      closed_sheet[f"W{closed_row}"] = item.operational_requirement  # Operational Requirement
      closed_sheet[f"X{closed_row}"] = item.deviation_rationale  # Deviation Rationale
      closed_sheet[f"Y{closed_row}"] = item.supporting_documents  # Supporting Documents
      closed_sheet[f"Z{closed_row}"] = item.comments  # Comments
      closed_sheet[f"AA{closed_row}"] = item.auto_approve  # Auto-Approve
      closed_sheet[f"AB{closed_row}"] = item.bod_22_01_tracking  # Binding Operational Directive 22-01 tracking
      closed_sheet[f"AC{closed_row}"] = datetime.strftime(item.bod_22_01_due_date, "%m/%d/%Y") if item.bod_22_01_due_date else ""  # Binding Operational Directive 22-01 Due Date
      closed_sheet[f"AD{closed_row}"] = item.cve  # CVE
      closed_sheet[f"AE{closed_row}"] = item.service_name  # Service Name
      closed_row += 1

    # Populate Configuration Findings
    config_row = 6
    for finding in configuration_findings:
      closed_sheet[f"A{closed_row}"] = item.id  # POAM ID
      closed_sheet[f"B{closed_row}"] = item.controls  # Controls
      closed_sheet[f"C{closed_row}"] = item.weakness_name  # Weakness Name
      closed_sheet[f"D{closed_row}"] = item.weakness_description  # Weakness Description
      closed_sheet[f"E{closed_row}"] = item.detector_source  # Weakness Detector Source
      closed_sheet[f"F{closed_row}"] = item.source_identifier  # Weakness Source Identifier
      closed_sheet[f"G{closed_row}"] = item.asset_identifier  # Asset Identifier
      closed_sheet[f"H{closed_row}"] = item.point_of_contact  # Point of Contact
      closed_sheet[f"I{closed_row}"] = item.resources_required  # Resources Required
      closed_sheet[f"J{closed_row}"] = item.remediation_plan  # Overall Remediation Plan
      closed_sheet[f"K{closed_row}"] = datetime.strftime(item.detection_date, "%m/%d/%Y") if item.detection_date else ""  # Original Detection Date
      closed_sheet[f"L{closed_row}"] = datetime.strftime(item.completion_date, "%m/%d/%Y") if item.completion_date else ""  # Scheduled Completion Date
      closed_sheet[f"M{closed_row}"] = item.planned_milestones  # Planned Milestones
      closed_sheet[f"N{closed_row}"] = item.milestone_changes  # Milestone Changes
      closed_sheet[f"O{closed_row}"] = datetime.strftime(item.status_date, "%m/%d/%Y") if item.status_date else ""  # Status Date
      closed_sheet[f"P{closed_row}"] = item.vendor_dependency  # Vendor Dependency
      closed_sheet[f"Q{closed_row}"] = datetime.strftime(item.vendor_checkin_date, "%m/%d/%Y") if item.vendor_checkin_date else ""  # Last Vendor Check-in Date
      closed_sheet[f"R{closed_row}"] = item.product_name  # Vendor Dependent Product Name
      closed_sheet[f"S{closed_row}"] = item.original_risk_rating  # Original Risk Rating
      closed_sheet[f"T{closed_row}"] = item.adjusted_risk_rating  # Adjusted Risk Rating
      closed_sheet[f"U{closed_row}"] = item.risk_adjustment  # Risk Adjustment
      closed_sheet[f"V{closed_row}"] = item.false_positive  # False Positive
      closed_sheet[f"W{closed_row}"] = item.operational_requirement  # Operational Requirement
      closed_sheet[f"X{closed_row}"] = item.deviation_rationale  # Deviation Rationale
      closed_sheet[f"Y{closed_row}"] = item.supporting_documents  # Supporting Documents
      closed_sheet[f"Z{closed_row}"] = item.comments  # Comments
      closed_sheet[f"AA{closed_row}"] = item.auto_approve  # Auto-Approve
      closed_sheet[f"AB{closed_row}"] = item.bod_22_01_tracking  # Binding Operational Directive 22-01 tracking
      closed_sheet[f"AC{closed_row}"] = datetime.strftime(item.bod_22_01_due_date, "%m/%d/%Y") if item.bod_22_01_due_date else ""  # Binding Operational Directive 22-01 Due Date
      closed_sheet[f"AD{closed_row}"] = item.cve  # CVE
      closed_sheet[f"AE{closed_row}"] = item.service_name  # Service Name
      closed_row += 1
      config_sheet[f"A{config_row}"] = finding.id  # POAM ID
      config_sheet[f"B{config_row}"] = finding.controls  # Controls
      config_sheet[f"C{config_row}"] = finding.weakness_name  # Weakness Name
      config_sheet[f"D{config_row}"] = finding.weakness_description  # Weakness Description
      config_sheet[f"E{config_row}"] = finding.detector_source  # Weakness Detector Source
      config_sheet[f"F{config_row}"] = finding.source_identifier  # Weakness Source Identifier
      config_sheet[f"G{config_row}"] = finding.asset_identifier  # Asset Identifier
      config_sheet[f"H{config_row}"] = finding.point_of_contact  # Point of Contact
      config_sheet[f"I{config_row}"] = finding.resources_required  # Resources Required
      config_sheet[f"J{config_row}"] = finding.remediation_plan  # Overall Remediation Plan
      config_sheet[f"K{config_row}"] = datetime.strftime(finding.detection_date, "%m/%d/%Y") if finding.detection_date else ""  # Original Detection Date
      config_sheet[f"L{config_row}"] = datetime.strftime(finding.completion_date, "%m/%d/%Y") if finding.completion_date else ""  # Scheduled Completion Date
      config_sheet[f"M{config_row}"] = finding.planned_milestones  # Planned Milestones
      config_sheet[f"N{config_row}"] = finding.milestone_changes  # Milestone Changes
      config_sheet[f"O{config_row}"] = datetime.strftime(finding.status_date, "%m/%d/%Y") if finding.status_date else ""  # Status Date
      config_sheet[f"P{config_row}"] = finding.vendor_dependency  # Vendor Dependency
      config_sheet[f"Q{config_row}"] = datetime.strftime(finding.vendor_checkin_date, "%m/%d/%Y") if finding.vendor_checkin_date else ""  # Last Vendor Check-in Date
      config_sheet[f"R{config_row}"] = finding.product_name  # Vendor Dependent Product Name
      config_sheet[f"S{config_row}"] = finding.original_risk_rating  # Original Risk Rating
      config_sheet[f"T{config_row}"] = finding.adjusted_risk_rating  # Adjusted Risk Rating
      config_sheet[f"U{config_row}"] = finding.risk_adjustment  # Risk Adjustment
      config_sheet[f"V{config_row}"] = finding.false_positive  # False Positive
      config_sheet[f"W{config_row}"] = finding.operational_requirement  # Operational Requirement
      config_sheet[f"X{config_row}"] = finding.deviation_rationale  # Deviation Rationale
      config_sheet[f"Y{config_row}"] = finding.supporting_documents  # Supporting Documents
      config_sheet[f"Z{config_row}"] = finding.comments  # Comments
      config_sheet[f"AA{config_row}"] = finding.auto_approve  # Auto-Approve
      config_sheet[f"AB{config_row}"] = finding.bod_22_01_tracking  # Binding Operational Directive 22-01 tracking
      config_sheet[f"AC{config_row}"] = datetime.strftime(finding.bod_22_01_due_date, "%m/%d/%Y") if finding.bod_22_01_due_date else ""  # Binding Operational Directive 22-01 Due Date
      config_sheet[f"AD{config_row}"] = finding.cve  # CVE
      config_sheet[f"AE{config_row}"] = finding.service_name  # Service Name
      config_row += 1

    # Save the populated template
    output_path = "Exported_FedRAMP_POAM.xlsx"
    workbook.save(output_path)
    return output_path

def get_configuration_findings():
    return ConfigurationFinding.query.all()

def get_poam_items():
    return POAM.query.all()

def get_assets_for_poam(poam_id):
    poam_item = POAM.query.get(poam_id)
    return poam_item.assets if poam_item else []

def link_asset_to_poam(poam_id, asset_data):
    poam_item = POAM.query.get(poam_id)
    if not poam_item:
        return None

    asset = Asset.query.filter_by(name=asset_data['name']).first()
    if not asset:
        asset = Asset(name=asset_data['name'], description=asset_data.get('description'))
        db.session.add(asset)

    poam_item.assets.append(asset)
    db.session.commit()
    return asset



  
