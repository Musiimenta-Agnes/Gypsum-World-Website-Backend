# 

from app.extensions import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    phone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)  # NEW field added
    password = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(50), default='customer') # 'senior_manager', 'viewer', 'customer'
    created_at = db.Column(db.DateTime, default=datetime.now)
    source = db.Column(db.String(20), default="Created Account")

    #  Profile fields
    profile_image = db.Column(db.String(255), nullable=True)  # store image path/URL
    address = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)












# from app.extensions import db
# from datetime import datetime


# class User(db.Model):
#     __tablename__ = 'users'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(120))
#     phone = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=True)  # NEW field added
#     password = db.Column(db.String(128))
#     is_admin = db.Column(db.Boolean, default='customer')
#     created_at = db.Column(db.DateTime, default=datetime.now) 
#     source = db.Column(db.String(20), default="Created Account")  

