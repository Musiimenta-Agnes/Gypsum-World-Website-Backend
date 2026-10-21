# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from app.models.cart.cart_item_model import CartItem
# from app.models.product.product_model import Product
# from app.models.user.user_model import User
# from app.extensions import db

# cart_bp = Blueprint('cart', __name__, url_prefix='/api/cart')


# # ✅ Add product to cart
# @cart_bp.route('/add_cart', methods=['POST'])
# @jwt_required()
# def add_to_cart():
#     user_id = get_jwt_identity()
#     user = User.query.get(user_id)

    
#     data = request.get_json()
#     if not data:
#         return jsonify({"error": "Missing JSON data"}), 400

#     product_id = data.get('product_id')
#     quantity = data.get('quantity', 1)

#     if not product_id:
#         return jsonify({"error": "Product ID is required"}), 400

#     product = Product.query.get(product_id)
#     if not product:
#         return jsonify({"error": "Product not found"}), 404

#     cart_item = CartItem(user_id=user.id, product_id=product.id, quantity=quantity)
#     db.session.add(cart_item)
#     db.session.commit()

#     subtotal = product.price * quantity
#     cart_items = CartItem.query.filter_by(user_id=user.id).all()
#     total_price = sum(item.product.price * item.quantity for item in cart_items)

#     return jsonify({
#         "message": "Product added to cart successfully",
#         "item": {
#             "product_name": product.name,
#             "quantity": quantity,
#             "price": product.price,
#             "subtotal": subtotal
#         },
#         "total_price": total_price
#     }), 201





# # ✅ Remove from cart
# @cart_bp.route('/remove/<int:cart_item_id>', methods=['DELETE'])
# @jwt_required()
# def remove_from_cart(cart_item_id):
#     user_id = get_jwt_identity()
#     user = User.query.get(user_id)

#     if user.is_admin:
#         return jsonify({"error": "Only customers can remove items from the cart"}), 403

#     cart_item = CartItem.query.filter_by(id=cart_item_id, user_id=user.id).first()
#     if not cart_item:
#         return jsonify({"error": "Cart item not found"}), 404

#     db.session.delete(cart_item)
#     db.session.commit()

#     return jsonify({"message": "Item removed from cart"}), 200






# # ✅ View all items in cart
# @cart_bp.route('/view_items_in_cart', methods=['GET'])
# @jwt_required()
# def view_all_items_in_cart():
#     user_id = get_jwt_identity()
#     cart_items = CartItem.query.filter_by(user_id=user_id).all()

#     items = []
#     total_price = 0

#     for item in cart_items:
#         product = Product.query.get(item.product_id)
#         subtotal = product.price * item.quantity
#         total_price += subtotal

#         items.append({
#             "cart_item_id": item.id,
#             "product_id": item.product_id,
#             "product_name": product.name,
#             "price": product.price,
#             "quantity": item.quantity,
#             "subtotal": subtotal
#         })

#     return jsonify({
#         "items": items,
#         "total_price": total_price
#     }), 200
