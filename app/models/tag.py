from app.extensions import db
import re

class Tag(db.Model):
    id = db.Column(db.String(50), primary_key=True)  # URL-safe, lowercase
    name = db.Column(db.String(50), unique=True, nullable=False)  # Human-readable

    def __init__(self, name):
        self.name = name
        self.id = self.generate_id(name)

    @staticmethod
    def generate_id(name):
        # Convert to lowercase, replace spaces with hyphens, remove non-alphanumeric characters
        return re.sub(r'[^a-z0-9-]', '', name.lower().replace(' ', '-'))

    def __repr__(self):
        return f'<Tag {self.name}>'
