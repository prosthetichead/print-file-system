from app.extensions import db

print_tags = db.Table('print_tags',
    db.Column('print_id', db.Integer, db.ForeignKey('print.id'), primary_key=True),
    db.Column('tag_id', db.String(50), db.ForeignKey('tag.id'), primary_key=True)
)

class Print(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.string(255), db.ForeignKey('creator.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    safe_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    modified_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    tags = db.relationship('Tag', secondary=print_tags, backref=db.backref('prints', lazy='dynamic'))
    files = db.relationship('PrintFile', back_populates='print_record', lazy='dynamic')

    creator = db.relationship('Creator', back_populates='prints')

    def __repr__(self):
        return f"<Print {self.name}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'modified_at': self.modified_at.isoformat(),
            'tags': [tag.name for tag in self.tags],
            'files': [file.to_dict() for file in self.files]
        }

    def to_simple_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'safe_name': self.safe_name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'modified_at': self.modified_at.isoformat(),
            'tags': [tag.name for tag in self.tags]
        }

    def dir_name(self, naming_pattern="{creator}/{name}#{id}"):
        return naming_pattern.format(
            creator=self.creator,
            name=self.name,
            id=self.id
        )
    