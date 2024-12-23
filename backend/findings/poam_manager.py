from openpyxl import load_workbook
from flask import send_file
from datetime import datetime
import os
from models import POAM, Finding  # Import database models
import pandas as pd
from models import ConfigurationFinding
TEMPLATE_PATH = "/mnt/data/FedRAMP-POAM-Template.xlsx"

def export_poam_with_template():
    """
    Populates the FedRAMP PO&AM Template with data for Open POA&M Items, Closed POA&M Items, and Configuration Findings.
    """
    # Load the Excel template
    workbook = load_workbook(TEMPLATE_PATH)

    # Sheets from the template
    open_sheet = workbook["Open POA&M Items"]
    closed_sheet = workbook["Closed POA&M Items"]
    config_sheet = workbook["Configuration Findings"]

    # Fetch POA&M items
    open_items = POAM.query.filter_by(status="Active").all()
    closed_items = POAM.query.filter_by(status="Resolved").all()

    # Fetch Configuration Findings
    configuration_findings = ConfigurationFinding.query.all()

    # Populate Open POA&M Items
    open_row = 2
    for item in open_items:
        open_sheet[f"A{open_row}"] = item.id
        open_sheet[f"B{open_row}"] = item.weakness
        open_sheet[f"C{open_row}"] = item.description
        open_sheet[f"D{open_row}"] = item.severity
        open_sheet[f"E{open_row}"] = item.status
        open_sheet[f"F{open_row}"] = datetime.strftime(item.detection_date, "%m/%d/%Y") if item.detection_date else ""
        open_sheet[f"G{open_row}"] = datetime.strftime(item.last_updated, "%m/%d/%Y") if item.last_updated else ""
        open_sheet[f"H{open_row}"] = item.product_name
        open_sheet[f"I{open_row}"] = item.risk_rating
        open_sheet[f"J{open_row}"] = item.detector_source
        open_row += 1

    # Populate Closed POA&M Items
    closed_row = 2
    for item in closed_items:
        closed_sheet[f"A{closed_row}"] = item.id
        closed_sheet[f"B{closed_row}"] = item.weakness
        closed_sheet[f"C{closed_row}"] = item.description
        closed_sheet[f"D{closed_row}"] = item.severity
        closed_sheet[f"E{closed_row}"] = item.status
        closed_sheet[f"F{closed_row}"] = datetime.strftime(item.detection_date, "%m/%d/%Y") if item.detection_date else ""
        closed_sheet[f"G{closed_row}"] = datetime.strftime(item.last_updated, "%m/%d/%Y") if item.last_updated else ""
        closed_sheet[f"H{closed_row}"] = item.product_name
        closed_sheet[f"I{closed_row}"] = item.risk_rating
        closed_sheet[f"J{closed_row}"] = item.detector_source
        closed_row += 1

    # Populate Configuration Findings
    config_row = 2
    for finding in configuration_findings:
        config_sheet[f"A{config_row}"] = finding.id
        config_sheet[f"B{config_row}"] = finding.description
        config_sheet[f"C{config_row}"] = finding.severity
        config_sheet[f"D{config_row}"] = datetime.strftime(finding.detection_date, "%m/%d/%Y")
        config_sheet[f"E{config_row}"] = finding.product_name
        config_row += 1

    # Save the populated template
    output_path = "Exported_FedRAMP_POAM.xlsx"
    workbook.save(output_path)
    return output_path
def get_configuration_findings():
    """
    Fetch all configuration findings from the database.
    """
    return ConfigurationFinding.query.all()


def get_open_poams():
    return POAM.query.filter_by(status="Active").all()


