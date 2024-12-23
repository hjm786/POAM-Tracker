import pandas as pd

def generate_scan_results_excel(scan_id):
    findings = Finding.query.filter_by(poam_id=scan_id).all()

    # Convert to DataFrame
    findings_df = pd.DataFrame([{
        "Tool": finding.tool,
        "Severity": finding.severity,
        "Description": finding.description,
        "Detection Date": finding.detection_date,
        "Status": "Resolved" if finding.is_resolved else "Active"
    } for finding in findings])

    # Create Excel file
    file_path = f"scan_results_{scan_id}.xlsx"
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        findings_df.to_excel(writer, sheet_name="Scan Results", index=False)

    return file_path
