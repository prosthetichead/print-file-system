from app.extensions import db

class PrintFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    print_id = db.Column(db.Integer, db.ForeignKey('print.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(4096), nullable=False)
    file_type = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    modified_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    print_record = db.relationship('Print', back_populates='files')



