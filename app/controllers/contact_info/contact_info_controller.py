# routes/contact.py
from flask import Blueprint, request, jsonify
from app.models.contact_info.contact_info_model import ContactInfo
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user.user_model import User

contact_bp = Blueprint('contact_bp', __name__, url_prefix='/api/contact')

@contact_bp.route('/get', methods=['GET'])
def get_contact_info():
    contact = ContactInfo.query.first()
    if not contact:
        return jsonify({"error": "No contact info found"}), 404

    return jsonify({
        "phone": contact.phone,
        "email": contact.email,
        "whatsapp": contact.whatsapp,
        "location": contact.location,
        "facebook": contact.facebook,
        "instagram": contact.instagram,
        "twitter": contact.twitter,
        "linkedin": contact.linkedin
    }), 200

# update contact info
@contact_bp.route('/update', methods=['PUT'])
def update_contact_info():
    data = request.json
    contact = ContactInfo.query.first()

    if not contact:
        contact = ContactInfo()

    contact.phone = data.get("phone", contact.phone)
    contact.email = data.get("email", contact.email)
    contact.whatsapp = data.get("whatsapp", contact.whatsapp)
    contact.location = data.get("location", contact.location)

    # Handle new social links
    contact.facebook = data.get("facebook", contact.facebook)
    contact.instagram = data.get("instagram", contact.instagram)
    contact.twitter = data.get("twitter", contact.twitter)
    contact.linkedin = data.get("linkedin", contact.linkedin)

    db.session.add(contact)
    db.session.commit()

    return jsonify({"message": "Contact info updated successfully"})
