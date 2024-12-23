import pytest
from flask import template_rendered
from contextlib import contextmanager
from views import main_bp
from flask import Flask

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(main_bp)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@contextmanager
def captured_templates(app):
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

def test_dashboard(client):
    response = client.get('/')
    assert response.status_code == 200

def test_get_scans(client):
    response = client.get('/scans')
    assert response.status_code == 200
    expected_scans = [
        {"id": 1, "name": "AWS Inspector - Critical"},
        {"id": 2, "name": "Tenable - Configuration"}
    ]
    assert b'AWS Inspector - Critical' in response.data
    assert b'Tenable - Configuration' in response.data

def test_get_scan_results(client):
    response = client.get('/scan-results?scan=1&page=1')
    assert response.status_code == 200
    assert b'AWS Inspector' in response.data
    assert b'Critical vulnerability' in response.data

def test_scan_results_pagination(client):
    # Test first page
    response = client.get('/scan-results?page=1')
    assert response.status_code == 200
    assert b'next' in response.data
    assert b'prev' not in response.data

    # Test middle page
    response = client.get('/scan-results?page=2')
    assert response.status_code == 200
    assert b'next' in response.data
    assert b'prev' in response.data

    # Test last page
    response = client.get('/scan-results?page=4')
    assert response.status_code == 200
    assert b'next' not in response.data
    assert b'prev' in response.data

def test_integrations(client):
    response = client.get('/integrations')
    assert response.status_code == 200
    assert b'AWS Inspector' in response.data
    assert b'Tenable' in response.data
    assert b'GitHub' in response.data
    assert b'Google Space' in response.data

def test_get_config_template(client):
    # Test AWS Inspector config template
    response = client.get('/integrations/aws_inspector/config-template')
    assert response.status_code == 200
    assert response.json['fields'][0]['name'] == 'access_key'
    
    # Test Tenable config template
    response = client.get('/integrations/tenable/config-template')
    assert response.status_code == 200
    assert 'scanner_type' in [field['name'] for field in response.json['fields']]
    
    # Test invalid integration
    response = client.get('/integrations/invalid/config-template')
    assert response.status_code == 200
    assert response.json == {'fields': []}