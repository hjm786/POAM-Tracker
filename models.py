from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Many-to-Many Association Table
poam_assets = db.Table(
    'poam_assets',
    db.Column('poam_id', db.Integer, db.ForeignKey('poam.id'), primary_key=True),
    db.Column('asset_id', db.Integer, db.ForeignKey('assets.id'), primary_key=True)
)

class Integration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tool = db.Column(db.String(50), nullable=False)
    details = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Finding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tool = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    detection_date = db.Column(db.DateTime, nullable=False)
    is_resolved = db.Column(db.Boolean, default=False)
    poam_id = db.Column(db.Integer, db.ForeignKey('poam.id'))

class ConfigurationFinding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poam_id = db.Column(db.String(50), nullable=False)
    controls = db.Column(db.String(255), nullable=True)
    weakness_name = db.Column(db.String(255), nullable=False)
    weakness_description = db.Column(db.Text, nullable=True)
    detector_source = db.Column(db.String(50), nullable=True)
    source_identifier = db.Column(db.String(50), nullable=True)
    asset_identifier = db.Column(db.Text, nullable=True)
    point_of_contact = db.Column(db.String(100), nullable=True)
    resources_required = db.Column(db.String(255), nullable=True)
    remediation_plan = db.Column(db.Text, nullable=True)
    detection_date = db.Column(db.DateTime, nullable=True)
    completion_date = db.Column(db.DateTime, nullable=True)
    planned_milestones = db.Column(db.Text, nullable=True)
    milestone_changes = db.Column(db.Text, nullable=True)
    status_date = db.Column(db.DateTime, nullable=True)
    vendor_dependency = db.Column(db.String(10), nullable=True)
    vendor_checkin_date = db.Column(db.DateTime, nullable=True)
    product_name = db.Column(db.String(255), nullable=True)
    original_risk_rating = db.Column(db.String(50), nullable=True)
    adjusted_risk_rating = db.Column(db.String(50), nullable=True)
    risk_adjustment = db.Column(db.String(10), nullable=True)
    false_positive = db.Column(db.String(10), nullable=True)
    operational_requirement = db.Column(db.String(10), nullable=True)
    deviation_rationale = db.Column(db.Text, nullable=True)
    supporting_documents = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)
    auto_approve = db.Column(db.String(10), nullable=True)
    bod_22_01_tracking = db.Column(db.String(10), nullable=True)
    bod_22_01_due_date = db.Column(db.DateTime, nullable=True)
    cve = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<ConfigurationFinding {self.id} - {self.weakness_name}>"

class Asset(db.Model):
    __tablename__ = 'assets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    owner = db.Column(db.String(100), nullable=True)
    asset_type = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationship to POA&M items
    poam_items = db.relationship('POAM', secondary='poam_assets', back_populates='assets')

    def __repr__(self):
        return f"<Asset {self.id} - {self.name}>"

class POAM(db.Model):
    __tablename__ = 'poam'
    id = db.Column(db.Integer, primary_key=True)
    controls = db.Column(db.String(255), nullable=True)
    weakness_name = db.Column(db.String(255), nullable=False)
    weakness_description = db.Column(db.Text, nullable=True)
    detector_source = db.Column(db.String(50), nullable=True)
    source_identifier = db.Column(db.String(50), nullable=True)
    asset_identifier = db.Column(db.Text, nullable=True)
    point_of_contact = db.Column(db.String(100), nullable=True)
    resources_required = db.Column(db.String(255), nullable=True)
    remediation_plan = db.Column(db.Text, nullable=True)
    detection_date = db.Column(db.DateTime, nullable=True)
    completion_date = db.Column(db.DateTime, nullable=True)
    planned_milestones = db.Column(db.Text, nullable=True)
    milestone_changes = db.Column(db.Text, nullable=True)
    status_date = db.Column(db.DateTime, nullable=True)
    vendor_dependency = db.Column(db.String(10), nullable=True)
    vendor_checkin_date = db.Column(db.DateTime, nullable=True)
    product_name = db.Column(db.String(255), nullable=True)
    original_risk_rating = db.Column(db.String(50), nullable=True)
    adjusted_risk_rating = db.Column(db.String(50), nullable=True)
    risk_adjustment = db.Column(db.String(10), nullable=True)
    false_positive = db.Column(db.String(10), nullable=True)
    operational_requirement = db.Column(db.String(10), nullable=True)
    deviation_rationale = db.Column(db.Text, nullable=True)
    supporting_documents = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)
    auto_approve = db.Column(db.String(10), nullable=True)
    bod_22_01_tracking = db.Column(db.String(10), nullable=True)
    bod_22_01_due_date = db.Column(db.DateTime, nullable=True)
    cve = db.Column(db.String(255), nullable=True)
    service_name = db.Column(db.Text, nullable=True)

    # Relationship to Assets
    assets = db.relationship('Asset', secondary='poam_assets', back_populates='poam_items')

    # Track last updated timestamp
    last_updated = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    status = db.Column(db.String(20), default="Active")

    def __repr__(self):
        return f"<POAM {self.id} - {self.weakness_name}>"

def initialize_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()