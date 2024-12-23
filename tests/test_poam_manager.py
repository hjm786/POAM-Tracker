import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from poam_manager import export_poam_with_template, get_configuration_findings, get_poam_items, get_assets_for_poam, link_asset_to_poam
from models import POAM, ConfigurationFinding, Asset, db

class TestPOAMManager(unittest.TestCase):
    def setUp(self):
        self.mock_poam = MagicMock()
        self.mock_poam.id = 1
        self.mock_poam.controls = "AC-1"
        self.mock_poam.weakness_name = "Test Weakness"
        self.mock_poam.weakness_description = "Test Description"
        self.mock_poam.status = "Active"
        self.mock_poam.detection_date = datetime(2023, 1, 1)
        
        self.mock_finding = MagicMock()
        self.mock_finding.id = 1
        self.mock_finding.controls = "AC-2"
        
        self.mock_asset = MagicMock()
        self.mock_asset.name = "Test Asset"
        self.mock_asset.description = "Test Asset Description"

    @patch('poam_manager.load_workbook')
    @patch('poam_manager.POAM')
    @patch('poam_manager.ConfigurationFinding')
    def test_export_poam_with_template(self, mock_config_finding, mock_poam, mock_load_workbook):
        mock_workbook = MagicMock()
        mock_sheet = MagicMock()
        mock_workbook.__getitem__.return_value = mock_sheet
        mock_load_workbook.return_value = mock_workbook
        
        mock_poam.query.filter_by().all.return_value = [self.mock_poam]
        mock_config_finding.query.all.return_value = [self.mock_finding]

        result = export_poam_with_template()
        
        self.assertEqual(result, "Exported_FedRAMP_POAM.xlsx")
        mock_workbook.save.assert_called_once()

    @patch('poam_manager.ConfigurationFinding')
    def test_get_configuration_findings(self, mock_config_finding):
        mock_config_finding.query.all.return_value = [self.mock_finding]
        
        findings = get_configuration_findings()
        
        self.assertEqual(findings, [self.mock_finding])
        mock_config_finding.query.all.assert_called_once()

    @patch('poam_manager.POAM')
    def test_get_poam_items(self, mock_poam):
        mock_poam.query.all.return_value = [self.mock_poam]
        
        items = get_poam_items()
        
        self.assertEqual(items, [self.mock_poam])
        mock_poam.query.all.assert_called_once()

    @patch('poam_manager.POAM')
    def test_get_assets_for_poam(self, mock_poam):
        mock_poam.query.get.return_value = self.mock_poam
        self.mock_poam.assets = [self.mock_asset]
        
        assets = get_assets_for_poam(1)
        
        self.assertEqual(assets, [self.mock_asset])
        mock_poam.query.get.assert_called_once_with(1)

    @patch('poam_manager.POAM')
    @patch('poam_manager.Asset')
    @patch('poam_manager.db.session')
    def test_link_asset_to_poam(self, mock_session, mock_asset, mock_poam):
        mock_poam.query.get.return_value = self.mock_poam
        mock_asset.query.filter_by().first.return_value = self.mock_asset
        
        asset_data = {
            'name': 'Test Asset',
            'description': 'Test Asset Description'
        }
        
        result = link_asset_to_poam(1, asset_data)
        
        self.assertEqual(result, self.mock_asset)
        mock_poam.query.get.assert_called_once_with(1)
        mock_session.commit.assert_called_once()

    @patch('poam_manager.POAM')
    def test_link_asset_to_poam_no_poam(self, mock_poam):
        mock_poam.query.get.return_value = None
        
        result = link_asset_to_poam(1, {'name': 'Test'})
        
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()