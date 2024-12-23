from flask_sqlalchemy import SQLAlchemy

from datetime import datetime


db = SQLAlchemy()

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


class POAM(db.Model):
    __tablename__ = 'poam'
    id = db.Column(db.Integer, primary_key=True)  # Unique Identifier
    controls = db.Column(db.String(255), nullable=True)  # Applicable 800-53 Control(s)
    weakness_name = db.Column(db.String(255), nullable=False)  # Name of the weakness
    weakness_description = db.Column(db.Text, nullable=True)  # Description of the weakness
    detector_source = db.Column(db.String(50), nullable=True)  # Scanner or source
    source_identifier = db.Column(db.String(50), nullable=True)  # Plugin ID or identifier
    asset_identifier = db.Column(db.Text, nullable=True)  # Unique asset identifier
    point_of_contact = db.Column(db.String(100), nullable=True)  # Responsible person
    resources_required = db.Column(db.String(255), nullable=True)  # Resources needed
    remediation_plan = db.Column(db.Text, nullable=True)  # Remediation plan overview
    detection_date = db.Column(db.DateTime, nullable=True)  # Original detection date
    completion_date = db.Column(db.DateTime, nullable=True)  # Scheduled completion date
    planned_milestones = db.Column(db.Text, nullable=True)  # Planned milestones
    milestone_changes = db.Column(db.Text, nullable=True)  # Changes to milestones
    status_date = db.Column(db.DateTime, nullable=True)  # Date of last status update
    vendor_dependency = db.Column(db.String(10), nullable=True)  # Yes/No for vendor dependency
    vendor_checkin_date = db.Column(db.DateTime, nullable=True)  # Last vendor check-in
    product_name = db.Column(db.String(255), nullable=True)  # Vendor-dependent product name
    original_risk_rating = db.Column(db.String(50), nullable=True)  # Original risk rating
    adjusted_risk_rating = db.Column(db.String(50), nullable=True)  # Adjusted risk rating
    risk_adjustment = db.Column(db.String(10), nullable=True)  # Risk adjustment (Yes/No)
    false_positive = db.Column(db.String(10), nullable=True)  # False positive (Yes/No)
    operational_requirement = db.Column(db.String(10), nullable=True)  # Operational requirement
    deviation_rationale = db.Column(db.Text, nullable=True)  # Deviation rationale
    supporting_documents = db.Column(db.Text, nullable=True)  # Supporting documents
    comments = db.Column(db.Text, nullable=True)  # Additional comments
    auto_approve = db.Column(db.String(10), nullable=True)  # Auto-approve (Yes/No)
    bod_22_01_tracking = db.Column(db.String(10), nullable=True)  # BOD 22-01 tracking (Yes/No)
    bod_22_01_due_date = db.Column(db.DateTime, nullable=True)  # BOD 22-01 due date
    cve = db.Column(db.String(255), nullable=True)  # Associated CVE numbers
    service_name = db.Column(db.Text, nullable=True)  # Service name (e.g., CSP's system)

    # Track last updated timestamp
    last_updated = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    status = db.Column(db.String(20), default="Active")  # POAM item status (Active/Resolved)

    def __repr__(self):
        return f"<POAM {self.id} - {self.weakness_name}>"

def initialize_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()







