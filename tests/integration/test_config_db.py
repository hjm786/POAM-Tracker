import unittest
from models import db
from integrations.config_db import IntegrationConfig, get_integration_config, set_integration_config
from flask import Flask

class TestIntegrationConfig(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(cls.app)
        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.drop_all()

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.session.begin(subtransactions=True)

    def tearDown(self):
        db.session.rollback()
        self.app_context.pop()

    def test_set_and_get_integration_config(self):
        integration_name = 'test_integration'
        config_data = {'key': 'value'}

        # Test setting the configuration
        set_integration_config(integration_name, config_data)
        config = IntegrationConfig.query.filter_by(integration_name=integration_name).first()
        self.assertIsNotNone(config)
        self.assertEqual(config.config_data, config_data)

        # Test getting the configuration
        retrieved_config = get_integration_config(integration_name)
        self.assertEqual(retrieved_config, config_data)

    def test_get_nonexistent_integration_config(self):
        integration_name = 'nonexistent_integration'
        retrieved_config = get_integration_config(integration_name)
        self.assertIsNone(retrieved_config)

    def test_update_integration_config(self):
        integration_name = 'test_integration'
        initial_config_data = {'key': 'initial_value'}
        updated_config_data = {'key': 'updated_value'}

        # Set initial configuration
        set_integration_config(integration_name, initial_config_data)
        config = IntegrationConfig.query.filter_by(integration_name=integration_name).first()
        self.assertEqual(config.config_data, initial_config_data)

        # Update configuration
        set_integration_config(integration_name, updated_config_data)
        config = IntegrationConfig.query.filter_by(integration_name=integration_name).first()
        self.assertEqual(config.config_data, updated_config_data)

if __name__ == '__main__':
    unittest.main()