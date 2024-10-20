from app.extensions import db

print_tags = db.Table('print_tags',
    db.Column('print_id', db.Integer, db.ForeignKey('print.id'), primary_key=True),
    db.Column('tag_id', db.String(50), db.ForeignKey('tag.id'), primary_key=True)
)

class Print(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    modified_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    tags = db.relationship('Tag', secondary=print_tags, backref=db.backref('prints', lazy='dynamic'))
    files = db.relationship('PrintFile', back_populates='print_record', lazy='dynamic')