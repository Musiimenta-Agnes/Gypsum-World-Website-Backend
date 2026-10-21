from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import jsonify
from app.models.user.user_model import User

def role_required(allowed_roles):
    """
    Protect a route so that only users with specific roles can access it.
    Example:
        @role_required(['senior_manager'])
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            try:
                user = User.query.get(int(user_id))
            except Exception:
                user = User.query.filter_by(phone=str(user_id)).first()

            if not user:
                return jsonify({"error": "User not found"}), 404

            # senior_manager has super admin access
            user_role = getattr(user, 'role', 'customer')
            if user_role not in allowed_roles and not (user.is_admin and 'senior_manager' in allowed_roles and user_role != 'viewer'):
                return jsonify({"error": "You do not have permission to perform this action. Edit rights are reserved for Senior Manager."}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

