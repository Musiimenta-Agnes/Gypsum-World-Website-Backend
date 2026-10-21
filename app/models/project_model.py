from datetime import datetime
from app.extensions import db

class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    image_url = db.Column(db.String(255))   # optional
    video_url = db.Column(db.String(255))   # optional
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
