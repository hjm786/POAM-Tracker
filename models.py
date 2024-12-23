from flask_sqlalchemy import SQLAlchemy

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

class POAM(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weakness = db.Column(db.String(255), nullable=False)
    severity = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), default="Active")
    last_updated = db.Column(db.DateTime, default=db.func.current_timestamp())

def initialize_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
