from flask import Flask 
from utils.database import db
from models import Employee
import os

app = Flask(__name__)

# Configuración de MongoDB
app.config['MONGODB_SETTINGS'] = {
    'db': 'minicore_pm',
    'host': 'localhost',
    'port': 27017
}

app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'a_default_secret_key_for_development')

db.init_app(app)

def load_user(user_id):
    return Employee.objects.get(id=user_id)

# Import the controllers
from controllers import main_blueprint
app.register_blueprint(main_blueprint)

if __name__ == "__main__":
    app.run(debug=True)