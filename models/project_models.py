from utils.database import db

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    tasks = db.relationship('Task', back_populates='project')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }
