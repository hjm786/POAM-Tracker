import pytest
from datetime import datetime
from flask import Flask
from models import db, Integration, Finding, ConfigurationFinding, Asset, POAM, initialize_db

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    initialize_db(app)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_integration_model(app):
    with app.app_context():
        integration = Integration(
            tool='test_tool',
            details={'key': 'value'}
        )
        db.session.add(integration)
        db.session.commit()
        
        assert integration.id is not None
        assert integration.tool == 'test_tool'
        assert integration.details == {'key': 'value'}
        assert integration.created_at is not None

def test_finding_model(app):
    with app.app_context():
        finding = Finding(
            tool='test_tool',
            severity='HIGH',
            description='Test finding',
            detection_date=datetime.now()
        )
        db.session.add(finding)
        db.session.commit()

        assert finding.id is not None
        assert finding.tool == 'test_tool'
        assert finding.severity == 'HIGH'
        assert finding.is_resolved is False

def test_asset_model(app):
    with app.app_context():
        asset = Asset(
            name='Test Asset',
            description='Test Description',
            owner='Test Owner',
            asset_type='Server'
        )
        db.session.add(asset)
        db.session.commit()

        assert asset.id is not None
        assert asset.name == 'Test Asset'
        assert str(asset) == f'<Asset {asset.id} - Test Asset>'

def test_poam_model(app):
    with app.app_context():
        poam = POAM(
            weakness_name='Test Weakness',
            weakness_description='Test Description',
            detector_source='Manual',
            status='Active'
        )
        db.session.add(poam)
        db.session.commit()

        assert poam.id is not None
        assert poam.weakness_name == 'Test Weakness'
        assert poam.status == 'Active'
        assert str(poam) == f'<POAM {poam.id} - Test Weakness>'

def test_poam_asset_relationship(app):
    with app.app_context():
        asset = Asset(name='Test Asset')
        poam = POAM(weakness_name='Test Weakness')
        
        poam.assets.append(asset)
        db.session.add(asset)
        db.session.add(poam)
        db.session.commit()

        assert asset in poam.assets
        assert poam in asset.poam_items

def test_configuration_finding_model(app):
    with app.app_context():
        finding = ConfigurationFinding(
            poam_id='123',
            weakness_name='Test Weakness',
            detector_source='Manual'
        )
        db.session.add(finding)
        db.session.commit()

        assert finding.id is not None
        assert finding.poam_id == '123'
        assert finding.weakness_name == 'Test Weakness'
        assert str(finding) == f'<ConfigurationFinding {finding.id} - Test Weakness>'