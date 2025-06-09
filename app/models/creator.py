from app.extensions import db, url_safe_value
import re

class Creator(db.Model):

    id = db.Column(db.String(255), primary_key=True)  # URL-safe, lowercase
    name = db.Column(db.String(255), unique=True, nullable=False)  # Human-readable
    description = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    modified_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    prints = db.relationship('Print', back_populates='creator', lazy='dynamic')

    def __init__(self, name):
        self.name = name
        self.id = url_safe_value(name)

    def __repr__(self):
        return f"<Creator {self.name}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'modified_at': self.modified_at.isoformat(),
            'prints': [print_record.to_simple_dict() for print_record in self.prints]
            }