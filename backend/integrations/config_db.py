from models import db

class IntegrationConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    integration_name = db.Column(db.String(50), nullable=False)
    config_data = db.Column(db.JSON, nullable=False)

def get_integration_config(integration_name):
    """
    Retrieve the configuration for a given integration.
    """
    config = IntegrationConfig.query.filter_by(integration_name=integration_name).first()
    return config.config_data if config else None

def set_integration_config(integration_name, config_data):
    """
    Save or update the configuration for a given integration.
    """
    config = IntegrationConfig.query.filter_by(integration_name=integration_name).first()
    if config:
        config.config_data = config_data
    else:
        config = IntegrationConfig(integration_name=integration_name, config_data=config_data)
        db.session.add(config)
    db.session.commit()
