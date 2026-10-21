
import os
import time
from flask import Blueprint, current_app, request, jsonify, send_from_directory
from app.models.product.product_model import db, Product
from app.models.user.user_model import User
from werkzeug.utils import secure_filename
from flask_jwt_extended import get_jwt_identity, jwt_required

product_bp = Blueprint('product', __name__, url_prefix='/api/products')

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp', 'tiff'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Flask backend route
@product_bp.route('/add_product', methods=['POST'])
@jwt_required()
def add_product():
    user = get_jwt_identity()

    name = request.form.get('name')
    page = request.form.get('page')
    image = request.files.get('image')

    if not name or not image or not page:
        return jsonify({'error': 'Name, image, and page are required'}), 400

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        unique_filename = f"{int(time.time() * 1000)}_{filename}"
        
        upload_folder = os.path.join(current_app.root_path, 'static/uploads')
        os.makedirs(upload_folder, exist_ok=True)

        print("Uploading to:", upload_folder)


        image_path = os.path.join(upload_folder, unique_filename)
        image.save(image_path)

        image_url = f'/static/uploads/{unique_filename}'

        product = Product(name=name, image_url=image_url, page=page)
        db.session.add(product)
        db.session.commit()

        return jsonify({'message': 'Product added successfully'}), 201

    return jsonify({'error': 'Invalid image'}), 400





# Route to get page for adding the product to
@product_bp.route('/by_page/<page_name>', methods=['GET'])
def get_products_by_page(page_name):
    products = Product.query.filter_by(page=page_name).all()
    return jsonify([p.serialize() for p in products])




# Get all products 
@product_bp.route('/get_all_products', methods=['GET'])
@jwt_required()
def get_all_products():
    products = Product.query.all()
    result = [
        {
            'id': p.id,
            'name': p.name,
            'image_url': p.image_url
        } for p in products
    ]
    return jsonify({'products': result}), 200  # Wrap in dict





# Update product 
@product_bp.route('/update_products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    try:
        user = get_jwt_identity()
        print("User:", user)


        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        name = request.form.get('name')
        image = request.files.get('image')

        print(f"Received name: {name}")
        print(f"Received image: {image.filename if image else 'No new image'}")

        if name:
            product.name = name

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            upload_folder = current_app.config.get('UPLOAD_FOLDER', 'static/uploads')
            os.makedirs(upload_folder, exist_ok=True)
            image_path = os.path.join(upload_folder, filename)
            image.save(image_path)
            product.image_url = f'/static/uploads/{filename}'

        db.session.commit()
        return jsonify({'message': 'Product updated successfully'}), 200

    except Exception as e:
        print("Update Exception:", str(e))  # For debugging
        return jsonify({'error': 'Something went wrong'}), 500





# Delete product
@product_bp.route('/delete_products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    user = get_jwt_identity()
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'}), 200


