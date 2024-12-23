import pytest
import pandas as pd
from unittest.mock import patch, Mock
from scan_manager import generate_scan_results_excel
import os

@pytest.fixture
def mock_findings():
    finding1 = Mock(
        tool="Nessus",
        severity="High",
        description="Test finding 1",
        detection_date="2023-01-01",
        is_resolved=True
    )
    finding2 = Mock(
        tool="OpenVAS", 
        severity="Medium",
        description="Test finding 2",
        detection_date="2023-01-02",
        is_resolved=False
    )
    return [finding1, finding2]

@pytest.fixture
def mock_query(mock_findings):
    with patch('scan_manager.Finding') as MockFinding:
        MockFinding.query.filter_by.return_value.all.return_value = mock_findings
        yield MockFinding

def test_generate_scan_results_excel(mock_query, mock_findings):
    scan_id = 123
    file_path = generate_scan_results_excel(scan_id)
    
    expected_path = f"scan_results_{scan_id}.xlsx"
    assert file_path == expected_path
    assert os.path.exists(file_path)
    
    # Verify Excel content
    df = pd.read_excel(file_path)
    assert len(df) == 2
    assert list(df.columns) == ["Tool", "Severity", "Description", "Detection Date", "Status"]
    
    # Verify first row
    assert df.iloc[0]["Tool"] == "Nessus"
    assert df.iloc[0]["Status"] == "Resolved"
    
    # Verify second row
    assert df.iloc[1]["Tool"] == "OpenVAS"
    assert df.iloc[1]["Status"] == "Active"
    
    # Cleanup
    os.remove(file_path)