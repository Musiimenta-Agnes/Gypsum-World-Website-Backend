from flask import Blueprint, request, jsonify, current_app, url_for
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
import uuid
import os
from app.extensions import db
from app.models.material_model import Material
from app.utils.auth_helpers import role_required

material_bp = Blueprint('material', __name__, url_prefix='/api/v1/materials')

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}

def allowed_file(filename, media_type):
    ext = filename.rsplit('.', 1)[1].lower()
    if media_type == 'image':
        return ext in ALLOWED_IMAGE_EXTENSIONS
    elif media_type == 'video':
        return ext in ALLOWED_VIDEO_EXTENSIONS
    return False

@material_bp.post('/')
@jwt_required()
@role_required(['admin'])
def add_material():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request'}), 400

    file = request.files['file']
    media_type = request.form.get('media_type', 'image').lower()

    if not file or file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if media_type not in ['image', 'video']:
        return jsonify({'error': 'media_type must be "image" or "video"'}), 400
    if not allowed_file(file.filename, media_type):
        return jsonify({'error': f'File type not allowed for {media_type}'}), 400

    filename = secure_filename(file.filename)
    save_folder = os.path.join(current_app.root_path,'static' ,'uploads', media_type)
    os.makedirs(save_folder, exist_ok=True)
    file_path = os.path.join(save_folder, filename)
    file.save(file_path)

    # Store URL relative to server
    media_url = url_for('static', filename=f'uploads/{media_type}/{filename}', _external=True)

    new_material = Material(media_url=media_url, media_type=media_type)
    db.session.add(new_material)
    db.session.commit()

    return jsonify({'message': f'{media_type.capitalize()} uploaded successfully', 'media_url': media_url}), 201

@material_bp.get('/')
# @jwt_required()
# @role_required(['admin', 'staff'])
def get_materials():
    materials = Material.query.all()
    result = [
        {'id': m.id, 'media_url': m.media_url, 'media_type': m.media_type}
        for m in materials
    ]
    return jsonify({'materials': result}), 200

@material_bp.get('/<int:material_id>')
# @jwt_required()
# @role_required(['admin', 'staff'])
def get_material(material_id):
    material = Material.query.get(material_id)
    if not material:
        return jsonify({'error': 'Material not found'}), 404
    return jsonify({'id': material.id, 'media_url': material.media_url, 'media_type': material.media_type}), 200


@material_bp.put('/<int:material_id>')
@jwt_required()
@role_required(['admin'])
def update_material(material_id):
    material = Material.query.get(material_id)
    if not material:
        return jsonify({'error': 'Material not found'}), 404

    # Optional new file
    if 'file' in request.files:
        file = request.files['file']
        media_type = request.form.get('media_type', material.media_type).lower()
        if file and allowed_file(file.filename, media_type):
            filename = secure_filename(file.filename)
            save_folder = os.path.join(current_app.root_path, 'uploads', media_type)
            os.makedirs(save_folder, exist_ok=True)
            file_path = os.path.join(save_folder, filename)
            file.save(file_path)
            material.media_url = url_for('static', filename=f'uploads/{media_type}/{filename}', _external=True)
            material.media_type = media_type

    db.session.commit()
    return jsonify({'message': 'Material updated successfully', 'media_url': material.media_url}), 200


@material_bp.delete('/<int:material_id>')
@jwt_required()
@role_required(['admin'])
def delete_material(material_id):
    material = Material.query.get(material_id)
    if not material:
        return jsonify({'error': 'Material not found'}), 404

    db.session.delete(material)
    db.session.commit()
    return jsonify({'message': 'Material deleted successfully'}), 200
