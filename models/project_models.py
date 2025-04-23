from utils.database import db

class Project(db.Document):
    name = db.StringField(required=True, max_length=100)
    description = db.StringField(required=True)

    meta = {'collection': 'projects'}

    def serialize(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description
        }
