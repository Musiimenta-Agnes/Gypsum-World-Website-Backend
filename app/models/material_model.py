from app.extensions import db

class Material(db.Model):
    __tablename__ = "materials"

    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(150), nullable=False)
    # description = db.Column(db.Text)
    media_url = db.Column(db.String(255), nullable=False)  # File path / URL
    media_type = db.Column(db.String(20), nullable=False)  # 'image' or 'video'
