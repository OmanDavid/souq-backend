from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Product

products_bp = Blueprint('products', __name__)

# GET all products (public) - supports ?category_id= filter
@products_bp.route('/products', methods=['GET'])
def get_products():
    category_id = request.args.get('category_id')
    query = Product.query
    if category_id:
        query = query.filter_by(category_id=category_id)
    products = query.all()
    return jsonify([{
        'id': p.id, 'title': p.title, 'price': p.price,
        'image_url': p.image_url, 'user_id': p.user_id,
        'category_id': p.category_id
    } for p in products]), 200

# GET single product (public)
@products_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    p = Product.query.get_or_404(id)
    return jsonify({
        'id': p.id, 'title': p.title, 'description': p.description,
        'price': p.price, 'image_url': p.image_url,
        'user_id': p.user_id, 'category_id': p.category_id
    }), 200

# POST new product (protected - only logged in users can list items)
@products_bp.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    product = Product(
        title=data['title'],
        description=data.get('description', ''),
        price=data['price'],
        image_url=data.get('image_url', ''),
        user_id=user_id,
        category_id=data['category_id']
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({'message': 'Product created', 'id': product.id}), 201

# PUT update product (protected - only the owner can edit)
@products_bp.route('/products/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    user_id = int(get_jwt_identity())
    product = Product.query.get_or_404(id)
    if product.user_id != user_id:
        return jsonify({'error': 'Not your product'}), 403
    data = request.get_json()
    product.title = data.get('title', product.title)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.image_url = data.get('image_url', product.image_url)
    db.session.commit()
    return jsonify({'message': 'Product updated'}), 200

# DELETE product (protected - only the owner can delete)
@products_bp.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    user_id = int(get_jwt_identity())
    product = Product.query.get_or_404(id)
    if product.user_id != user_id:
        return jsonify({'error': 'Not your product'}), 403
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'}), 200