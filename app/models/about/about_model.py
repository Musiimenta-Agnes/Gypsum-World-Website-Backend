# models/about.py
from app.extensions import db
class AboutContent(db.Model):

    __tablename__ = 'aboutus'


    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    mission = db.Column(db.Text)
    description = db.Column(db.Text)
    points = db.Column(db.JSON)  # List of [title, description]
    image_url = db.Column(db.String(255))
