from datetime import datetime
from app.extensions import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    page = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

# Serialise this
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'image': self.image_url,  # important: key must be 'image' to match frontend
            'page': self.page,
            'created_at': self.created_at.isoformat()
        }


# class Product(db.Model):
#     __tablename__ = 'products'


#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(120), nullable=False)
#     image_url = db.Column(db.String(255), nullable=False)  # store image URL/path
#     created_at = db.Column(db.DateTime, default=datetime.now)


    

   
       

