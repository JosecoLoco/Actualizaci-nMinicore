from utils.database import db

class Employee(db.Document):
    name = db.StringField(required=True, max_length=100)
    email = db.StringField(required=True, max_length=120, unique=True)
    role = db.StringField(required=True, max_length=50)

    meta = {'collection': 'employees'}

    def serialize(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "role": self.role
        }
