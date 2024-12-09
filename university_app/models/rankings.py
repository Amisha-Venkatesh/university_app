from utils.db import db

class University(db.Model):
    __tablename__ = 'universities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(50), nullable=False)
    discipline = db.Column(db.String(50), nullable=False)
    specialized_rankings = db.Column(db.String(100), nullable=False)
    alumni = db.Column(db.Integer, nullable=False)
    award = db.Column(db.Integer, nullable=False)
    hici = db.Column(db.Integer, nullable=False)
    n_s = db.Column(db.Integer, nullable=False)
    pub = db.Column(db.Integer, nullable=False)
    pcp = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
