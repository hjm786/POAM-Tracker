from flask import Flask
from models import db, initialize_db
from views import main_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
initialize_db(app)

# Register blueprints
app.register_blueprint(main_bp)

if __name__ == "__main__":
    app.run(debug=True)
