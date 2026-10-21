from flask import Blueprint, request, jsonify, current_app, url_for
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
import os
from app.extensions import db
from app.models.gallery_model import Gallery
from app.utils.auth_helpers import role_required

gallery_bp = Blueprint('gallery', __name__, url_prefix='/api/v1/gallery')

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}

def allowed_file(filename, media_type):
    ext = filename.rsplit('.', 1)[1].lower()
    if media_type == 'image':
        return ext in ALLOWED_IMAGE_EXTENSIONS
    elif media_type == 'video':
        return ext in ALLOWED_VIDEO_EXTENSIONS
    return False

# -----------------------------
# Add new media
# -----------------------------
@gallery_bp.post('/')
@jwt_required()
@role_required(['admin', 'staff'])
def add_media():
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
    save_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'gallery', media_type)
    os.makedirs(save_folder, exist_ok=True)
    file_path = os.path.join(save_folder, filename)
    file.save(file_path)

    media_url = url_for('static', filename=f'uploads/gallery/{media_type}/{filename}', _external=True)

    new_media = Gallery(media_url=media_url, media_type=media_type)
    db.session.add(new_media)
    db.session.commit()

    return jsonify({'message': f'{media_type.capitalize()} uploaded successfully', 'media_url': media_url}), 201

# -----------------------------
# Get all gallery media
# -----------------------------
@gallery_bp.get('/')
def get_media():
    items = Gallery.query.order_by(Gallery.created_at.desc()).all()
    result = [
        {'id': m.id, 'media_url': m.media_url, 'media_type': m.media_type}
        for m in items
    ]
    return jsonify({'gallery': result}), 200

# -----------------------------
# Get single media
# -----------------------------
@gallery_bp.get('/<int:media_id>')
def get_single_media(media_id):
    media = Gallery.query.get(media_id)
    if not media:
        return jsonify({'error': 'Media not found'}), 404
    return jsonify({
        'id': media.id,
        'media_url': media.media_url,
        'media_type': media.media_type
    }), 200
    

# -----------------------------
# Update gallery media
# -----------------------------
@gallery_bp.put('/<int:media_id>')
@jwt_required()
@role_required(['admin'])
def update_media(media_id):
    media = Gallery.query.get(media_id)
    if not media:
        return jsonify({'error': 'Media not found'}), 404

    # Optional new file
    if 'file' in request.files:
        file = request.files['file']
        media_type = request.form.get('media_type', media.media_type).lower()
        if file and allowed_file(file.filename, media_type):
            filename = secure_filename(file.filename)
            save_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'gallery', media_type)
            os.makedirs(save_folder, exist_ok=True)
            file_path = os.path.join(save_folder, filename)
            file.save(file_path)
            media.media_url = url_for('static', filename=f'uploads/gallery/{media_type}/{filename}', _external=True)
            media.media_type = media_type

    db.session.commit()
    return jsonify({'message': 'Gallery media updated successfully', 'media_url': media.media_url}), 200


# -----------------------------
# Delete media
# -----------------------------
@gallery_bp.delete('/<int:media_id>')
@jwt_required()
@role_required(['admin'])
def delete_media(media_id):
    media = Gallery.query.get(media_id)
    if not media:
        return jsonify({'error': 'Media not found'}), 404

    db.session.delete(media)
    db.session.commit()
    return jsonify({'message': 'Media deleted successfully'}), 200
