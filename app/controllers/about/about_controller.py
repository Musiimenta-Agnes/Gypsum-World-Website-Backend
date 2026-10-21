

from app.models.about.about_model import AboutContent,db
# routes/contact.py
import os
from app.models.contact_info.contact_info_model import ContactInfo
from app.extensions import db
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user.user_model import User

import time
from flask import Blueprint, current_app, request, jsonify, send_from_directory
from app.models.product.product_model import Product


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp', 'tiff'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




# Get the about us information
about_bp = Blueprint('about_bp', __name__, url_prefix='/api/about')

@about_bp.route('/get_about', methods=['GET'])
def get_about():
    content = AboutContent.query.first()
    if not content:
        return jsonify({'error': 'Content not found'}), 404

    return jsonify({
        'title': content.title,
        'mission': content.mission,
        'description': content.description,
        'points': content.points,
        'image_url': content.image_url
    })


#Update the about Us page
@about_bp.route('/update_about', methods=['PUT'])

def update_about():
    data = request.get_json()
    content = AboutContent.query.first()

    if not content:
        content = AboutContent()

    content.title = data.get('title')
    content.mission = data.get('mission')
    content.description = data.get('description')
    content.points = data.get('points', [])
    content.image_url = data.get('image_url')

    db.session.add(content)
    db.session.commit()
    return jsonify({'message': 'About page updated successfully'})




#Update or change the image
@about_bp.route('/about_upload-image', methods=['POST'])
def about_upload_image():
    image = request.files.get('image')
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        unique_filename = f"{int(time.time() * 1000)}_{filename}"

        # Path to static/uploads folder
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)

        image_path = os.path.join(upload_folder, unique_filename)
        image.save(image_path)

        # Return path relative to your Flask static folder
        image_url = f"/static/uploads/{unique_filename}"

        # Optional: save to DB if you want to track the image separately

        return jsonify({'image_url': image_url}), 201

    return jsonify({'error': 'Invalid image'}), 400
