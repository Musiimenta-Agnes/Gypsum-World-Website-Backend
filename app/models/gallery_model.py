from datetime import datetime
from app.extensions import db

class Gallery(db.Model):
    __tablename__ = "gallery"

    id = db.Column(db.Integer, primary_key=True)
    media_url = db.Column(db.String(255), nullable=False)  # Can store image or video URL
    media_type = db.Column(db.String(20), nullable=False)  # 'image' or 'video'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
