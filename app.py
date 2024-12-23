from flask import Flask
from models import db, initialize_db
from views import main_bp
from flask import render_template
from jinja2 import TemplateNotFound

app = Flask(
    __name__,
    static_folder="backend/static",      # Updated path for static files
    template_folder="backend/templates" # Updated path for templates
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
initialize_db(app)

# Register blueprints
app.register_blueprint(main_bp)

@app.errorhandler(TemplateNotFound)
def handle_missing_template(error):
    return render_template('error.html', message="Template not found. Please contact the administrator."), 404

if __name__ == "__main__":
    app.run(debug=True)