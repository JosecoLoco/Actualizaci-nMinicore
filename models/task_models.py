from utils.database import db
from datetime import datetime

class Task(db.Document):
    description = db.StringField(required=True, max_length=200)
    start_date = db.DateField(required=True)
    estimated_days = db.IntField(required=True)
    status = db.StringField(required=True, max_length=20)
    employee_id = db.ReferenceField('Employee', required=True)
    project_id = db.ReferenceField('Project', required=True)

    meta = {'collection': 'tasks'}

    def serialize(self):
        return {
            "id": str(self.id),
            "description": self.description,
            "start_date": self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
            "estimated_days": self.estimated_days,
            "status": self.status,
            "employee_id": str(self.employee_id.id),
            "project_id": str(self.project_id.id)
        }
