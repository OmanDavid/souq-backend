from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Order, Product

orders_bp = Blueprint('orders', __name__)

# GET all orders for the logged-in user (protected)
@orders_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    user_id = int(get_jwt_identity())
    orders = Order.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': o.id, 'status': o.status, 'total': o.total,
        'products': [p.id for p in o.products]
    } for o in orders]), 200

# GET single order (protected - only the owner can view)
@orders_bp.route('/orders/<int:id>', methods=['GET'])
@jwt_required()
def get_order(id):
    user_id = int(get_jwt_identity())
    order = Order.query.get_or_404(id)
    if order.user_id != user_id:
        return jsonify({'error': 'Not your order'}), 403
    return jsonify({
        'id': order.id, 'status': order.status, 'total': order.total,
        'products': [p.id for p in order.products]
    }), 200

# POST create order from cart items (protected)
@orders_bp.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    product_ids = data['product_ids']  # list of product ids being bought
    products = Product.query.filter(Product.id.in_(product_ids)).all()

    # block buying your own product
    for p in products:
        if p.user_id == user_id:
            return jsonify({'error': f'Cannot buy your own product: {p.title}'}), 400

    total = sum(p.price for p in products)
    order = Order(user_id=user_id, total=total, status='pending')
    order.products = products
    db.session.add(order)
    db.session.commit()
    return jsonify({'message': 'Order placed', 'id': order.id}), 201

# PUT update order status e.g. cancel (protected - only the owner)
@orders_bp.route('/orders/<int:id>', methods=['PUT'])
@jwt_required()
def update_order(id):
    user_id = int(get_jwt_identity())
    order = Order.query.get_or_404(id)
    if order.user_id != user_id:
        return jsonify({'error': 'Not your order'}), 403
    data = request.get_json()
    order.status = data.get('status', order.status)
    db.session.commit()
    return jsonify({'message': 'Order updated'}), 200

# DELETE cancel/remove an order (protected - only the owner)
@orders_bp.route('/orders/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_order(id):
    user_id = int(get_jwt_identity())
    order = Order.query.get_or_404(id)
    if order.user_id != user_id:
        return jsonify({'error': 'Not your order'}), 403
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted'}), 200