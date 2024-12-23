import unittest
from unittest.mock import patch, MagicMock
from integrations.tenable import fetch_tenable_findings, normalize_findings

class TestTenableIntegration(unittest.TestCase):

    @patch('integrations.tenable.get_integration_config')
    @patch('integrations.tenable.TenableIO')
    def test_fetch_tenable_findings(self, MockTenableIO, mock_get_integration_config):
        # Mock configuration
        mock_get_integration_config.return_value = {
            'access_key': 'fake_access_key',
            'secret_key': 'fake_secret_key',
            'domain': 'cloud.tenable.com'
        }

        # Mock TenableIO client and its response
        mock_tio_instance = MockTenableIO.return_value
        mock_tio_instance.vulns.list.return_value = [
            {
                'severity': 'High',
                'plugin_name': 'Example Vulnerability',
                'first_found': '2023-01-01T00:00:00Z',
                'state': 'OPEN'
            }
        ]

        findings = fetch_tenable_findings()
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]['tool'], 'Tenable')
        self.assertEqual(findings[0]['severity'], 'High')
        self.assertEqual(findings[0]['description'], 'Example Vulnerability')
        self.assertEqual(findings[0]['detection_date'], '2023-01-01T00:00:00Z')
        self.assertEqual(findings[0]['status'], 'Active')

    def test_normalize_findings(self):
        vulnerabilities = [
            {
                'severity': 'Medium',
                'plugin_name': 'Another Vulnerability',
                'first_found': '2023-02-01T00:00:00Z',
                'state': 'CLOSED'
            }
        ]

        normalized = normalize_findings(vulnerabilities)
        self.assertEqual(len(normalized), 1)
        self.assertEqual(normalized[0]['tool'], 'Tenable')
        self.assertEqual(normalized[0]['severity'], 'Medium')
        self.assertEqual(normalized[0]['description'], 'Another Vulnerability')
        self.assertEqual(normalized[0]['detection_date'], '2023-02-01T00:00:00Z')
        self.assertEqual(normalized[0]['status'], 'Resolved')

if __name__ == '__main__':
    unittest.main()