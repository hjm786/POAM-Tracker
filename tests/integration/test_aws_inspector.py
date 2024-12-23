import unittest
from unittest.mock import patch, MagicMock
from backend.integrations.aws_inspector import fetch_aws_inspector_findings, normalize_findings

class TestAWSInspectorIntegration(unittest.TestCase):

    @patch('backend.integrations.aws_inspector.get_integration_config')
    @patch('backend.integrations.aws_inspector.boto3.client')
    def test_fetch_aws_inspector_findings(self, mock_boto_client, mock_get_config):
        # Mock configuration
        mock_get_config.return_value = {
            'access_key': 'fake_access_key',
            'secret_key': 'fake_secret_key',
            'region': 'us-west-2'
        }

        # Mock boto3 client and its response
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client
        mock_client.list_findings.return_value = {
            'findings': [
                {
                    'severity': 'HIGH',
                    'title': 'Test finding',
                    'createdAt': MagicMock(strftime=lambda x: '2023-01-01')
                }
            ]
        }

        # Call the function
        findings = fetch_aws_inspector_findings()

        # Assertions
        mock_get_config.assert_called_once_with('aws_inspector')
        mock_boto_client.assert_called_once_with(
            'inspector2',
            aws_access_key_id='fake_access_key',
            aws_secret_access_key='fake_secret_key',
            region_name='us-west-2'
        )
        mock_client.list_findings.assert_called_once()
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]['tool'], 'AWS Inspector')
        self.assertEqual(findings[0]['severity'], 'HIGH')
        self.assertEqual(findings[0]['description'], 'Test finding')
        self.assertEqual(findings[0]['detection_date'], '2023-01-01')
        self.assertEqual(findings[0]['status'], 'Active')

    def test_normalize_findings(self):
        findings = [
            {
                'severity': 'MEDIUM',
                'title': 'Another test finding',
                'createdAt': MagicMock(strftime=lambda x: '2023-02-01')
            }
        ]
        normalized = normalize_findings(findings)
        self.assertEqual(len(normalized), 1)
        self.assertEqual(normalized[0]['tool'], 'AWS Inspector')
        self.assertEqual(normalized[0]['severity'], 'MEDIUM')
        self.assertEqual(normalized[0]['description'], 'Another test finding')
        self.assertEqual(normalized[0]['detection_date'], '2023-02-01')
        self.assertEqual(normalized[0]['status'], 'Active')

if __name__ == '__main__':
    unittest.main()