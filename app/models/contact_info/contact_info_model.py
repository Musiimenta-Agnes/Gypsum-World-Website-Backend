# # models/contact_info.py
# from app.extensions import db

# class ContactInfo(db.Model):
#     __tablename__ = 'contacts'


#     id = db.Column(db.Integer, primary_key=True)
#     phone = db.Column(db.String(50))
#     email = db.Column(db.String(120))
#     whatsapp = db.Column(db.String(50))
#     location = db.Column(db.String(255))



from app.extensions import db

class ContactInfo(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(50))
    email = db.Column(db.String(120))
    whatsapp = db.Column(db.String(50))
    location = db.Column(db.String(255))

    #  Add these new fields
    facebook = db.Column(db.String(255))
    instagram = db.Column(db.String(255))
    twitter = db.Column(db.String(255))
    linkedin = db.Column(db.String(255))
