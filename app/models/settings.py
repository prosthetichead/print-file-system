from app.extensions import db


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Settings {self.name}>'