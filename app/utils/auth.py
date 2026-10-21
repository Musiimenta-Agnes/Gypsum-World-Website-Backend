# from flask_jwt_extended import create_access_token
# from app.extensions import bcrypt
# from app.models.user.user_model import User


# def hash_password(password):
#     return bcrypt.generate_password_hash(password).decode('utf-8')

# def check_password(password, hashed):
#     return bcrypt.check_password_hash(hashed, password)

# def generate_token(user):
#     return create_access_token(identity=str(user.id))

