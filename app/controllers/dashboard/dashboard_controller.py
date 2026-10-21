from flask import Blueprint, jsonify
from app.models.user.user_model import User
from flask_jwt_extended import jwt_required, get_jwt_identity

dashboard_bp = Blueprint('dashboard_routes', __name__, url_prefix='/api/dashboard')

@dashboard_bp.route('/api/admin/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    current_user = User.query.get(get_jwt_identity())
    
    if not current_user or not current_user.is_admin:
        return jsonify({'error': 'Admins only'}), 403

    # return actual dashboard data
    return jsonify({'message': 'Welcome admin!'}), 200
