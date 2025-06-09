from app.extensions import db, url_safe_value
import re

class Tag(db.Model):
    id = db.Column(db.String(50), primary_key=True)  # URL-safe, lowercase
    name = db.Column(db.String(50), unique=True, nullable=False)  # Human-readable

    def __init__(self, name):
        self.name = name
        self.id = self.url_safe_value(name)

    def __repr__(self):
        return f'<Tag {self.name}>' 
