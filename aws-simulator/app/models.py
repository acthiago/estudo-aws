from app import db

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(256), nullable=False, unique=True)
    options = db.Column(db.PickleType, nullable=False)
    answer = db.Column(db.String(256), nullable=False)
    explanation = db.Column(db.String(512), nullable=False)
