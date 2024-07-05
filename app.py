from flask import Flask 
from utils.database import db
from models import Employee
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'a_default_secret_key_for_development')

db.init_app(app)

def load_user(user_id):
    return Employee.query.get(int(user_id))

with app.app_context():
    db.create_all() 

# Import the controllers
from controllers import main_blueprint
app.register_blueprint(main_blueprint)




if __name__ == "__main__":
    app.run(debug=True)