from utils.database import db
from datetime import datetime

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    estimated_days = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    
    employee = db.relationship('Employee', back_populates='tasks')
    project = db.relationship('Project', back_populates='tasks')

    def serialize(self):
        return {
            "id": self.id,
            "description": self.description,
            "start_date": self.start_date,
            "estimated_days": self.estimated_days,
            "status": self.status,
            "employee_id": self.employee_id,
            "project_id": self.project_id
        }
