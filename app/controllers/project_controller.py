import os
from flask import Blueprint, request, jsonify, current_app, url_for
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models.project_model import Project
from app.utils.auth_helpers import role_required
from datetime import datetime

project_bp = Blueprint('projects', __name__, url_prefix='/api/v1/projects')

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}

def allowed_file(filename, media_type):
    ext = filename.rsplit('.', 1)[1].lower()
    if media_type == 'image':
        return ext in ALLOWED_IMAGE_EXTENSIONS
    elif media_type == 'video':
        return ext in ALLOWED_VIDEO_EXTENSIONS
    return False

# -------------------------------
# CREATE PROJECT
# -------------------------------
@project_bp.post('/')
@jwt_required()
@role_required(['admin', 'staff'])
def create_project():
    title = request.form.get('title')
    if not title:
        return jsonify({"error": "title is required"}), 400

    image_file = request.files.get('image')
    video_file = request.files.get('video')

    image_url = None
    video_url = None

    # ---- IMAGE UPLOAD ----
    if image_file:
        if not allowed_file(image_file.filename, 'image'):
            return jsonify({"error": "Invalid image file type"}), 400

        filename = secure_filename(image_file.filename)
        save_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'projects', 'images')
        os.makedirs(save_folder, exist_ok=True)
        file_path = os.path.join(save_folder, filename)
        image_file.save(file_path)
        image_url = url_for('static', filename=f'uploads/projects/images/{filename}', _external=True)

    # ---- VIDEO UPLOAD ----
    if video_file:
        if not allowed_file(video_file.filename, 'video'):
            return jsonify({"error": "Invalid video file type"}), 400

        filename = secure_filename(video_file.filename)
        save_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'projects', 'videos')
        os.makedirs(save_folder, exist_ok=True)
        file_path = os.path.join(save_folder, filename)
        video_file.save(file_path)
        video_url = url_for('static', filename=f'uploads/projects/videos/{filename}', _external=True)

    new_project = Project(
        title=title,
        image_url=image_url,
        video_url=video_url,
    )

    db.session.add(new_project)
    db.session.commit()

    return jsonify({"message": "Project created successfully", "image_url": image_url, "video_url": video_url}), 201

# -------------------------------
# GET ALL PROJECTS
# -------------------------------
@project_bp.get('/')
def get_projects():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return jsonify([
        {
            "id": p.id,
            "title": p.title,
            "image_url": p.image_url,
            "video_url": p.video_url,
            "created_at": p.created_at
        }
        for p in projects
    ]), 200

# -------------------------------
# GET SINGLE PROJECT
# -------------------------------
@project_bp.get('/<int:id>')
def get_project(id):
    project = Project.query.get(id)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    return jsonify({
        "id": project.id,
        "title": project.title,
        "image_url": project.image_url,
        "video_url": project.video_url,
        "created_at": project.created_at
    }), 200

# -------------------------------
# UPDATE PROJECT
# -------------------------------
@project_bp.put('/<int:id>')
@jwt_required()
@role_required(['admin', 'staff'])
def update_project(id):
    project = Project.query.get(id)
    if not project:
        return jsonify({"error": "Project not found"}), 404

    title = request.form.get('title')
    if title:
        project.title = title

    image_file = request.files.get('image')
    video_file = request.files.get('video')

    if image_file and allowed_file(image_file.filename, 'image'):
        filename = secure_filename(image_file.filename)
        save_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'projects', 'images')
        os.makedirs(save_folder, exist_ok=True)
        file_path = os.path.join(save_folder, filename)
        image_file.save(file_path)
        project.image_url = url_for('static', filename=f'uploads/projects/images/{filename}', _external=True)

    if video_file and allowed_file(video_file.filename, 'video'):
        filename = secure_filename(video_file.filename)
        save_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'projects', 'videos')
        os.makedirs(save_folder, exist_ok=True)
        file_path = os.path.join(save_folder, filename)
        video_file.save(file_path)
        project.video_url = url_for('static', filename=f'uploads/projects/videos/{filename}', _external=True)

    db.session.commit()
    return jsonify({"message": "Project updated successfully", "image_url": project.image_url, "video_url": project.video_url}), 200

# -------------------------------
# DELETE PROJECT
# -------------------------------
@project_bp.delete('/<int:id>')
@jwt_required()
@role_required(['admin', 'staff'])
def delete_project(id):
    project = Project.query.get(id)
    if not project:
        return jsonify({"error": "Project not found"}), 404

    db.session.delete(project)
    db.session.commit()
    return jsonify({"message": "Project deleted successfully"}), 200
