from .extensions import db

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    channel = db.Column(db.String(50), nullable=False)
    sent = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Reminder {self.name}>'