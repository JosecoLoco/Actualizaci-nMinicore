from utils.database import db
from datetime import datetime

class Project(db.Document):
    name = db.StringField(required=True, max_length=100)
    description = db.StringField(required=True)
    end_date = db.DateField(required=True)
    status = db.StringField(required=True, default='Active')

    meta = {'collection': 'projects'}

    def serialize(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "end_date": self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            "status": self.status
        }
