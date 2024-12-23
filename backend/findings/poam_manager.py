from openpyxl import load_workbook
from flask import send_file
from datetime import datetime
import os
from models import POAM  # Import your database model for PO&AM items
import pandas as pd

# Path to the FedRAMP PO&AM Template
TEMPLATE_PATH = "/mnt/data/FedRAMP-POAM-Template.xlsx"

def export_poam_with_template():
    """
    Populates the provided FedRAMP PO&AM Template with data from the database.
    """
    # Load the Excel template
    workbook = load_workbook(TEMPLATE_PATH)
    active_sheet = workbook.active  # Assuming the first sheet is the one to populate

    # Fetch PO&AM items from the database
    poam_items = POAM.query.all()  # Replace with filtered queries if needed

    # Define the starting row
    row = 2  # Assuming the first row contains headers

    # Populate the template
    for item in poam_items:
        active_sheet[f"A{row}"] = item.id
        active_sheet[f"B{row}"] = item.weakness
        active_sheet[f"C{row}"] = item.description
        active_sheet[f"D{row}"] = item.severity
        active_sheet[f"E{row}"] = item.status
        active_sheet[f"F{row}"] = datetime.strftime(item.detection_date, "%m/%d/%Y") if item.detection_date else ""
        active_sheet[f"G{row}"] = datetime.strftime(item.last_updated, "%m/%d/%Y") if item.last_updated else ""
        active_sheet[f"H{row}"] = item.product_name
        active_sheet[f"I{row}"] = item.risk_rating
        active_sheet[f"J{row}"] = item.detector_source
        row += 1

    # Save the populated template
    output_path = "Exported_FedRAMP_POAM.xlsx"
    workbook.save(output_path)
    return output_path

def generate_poam_excel():
    """
    Generates an Excel file with active and resolved PO&AM items.
    """
    # Query active and resolved PO&AM items
    active_items = POAM.query.filter_by(status="Active").all()
    resolved_items = POAM.query.filter_by(status="Resolved").all()

    # Convert to DataFrame
    active_df = pd.DataFrame([{
        "ID": item.id,
        "Weakness": item.weakness,
        "Severity": item.severity,
        "Status": item.status,
        "Last Updated": item.last_updated
    } for item in active_items])

    resolved_df = pd.DataFrame([{
        "ID": item.id,
        "Weakness": item.weakness,
        "Severity": item.severity,
        "Status": item.status,
        "Last Updated": item.last_updated
    } for item in resolved_items])

    # Create Excel file
    file_path = "poam_items.xlsx"
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        active_df.to_excel(writer, sheet_name="Active Items", index=False)
        resolved_df.to_excel(writer, sheet_name="Resolved Items", index=False)

    return file_path
