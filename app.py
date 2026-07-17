from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import db
from auth import auth_bp
from products import products_bp
from orders import orders_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///souq.db'
app.config['JWT_SECRET_KEY'] = 'change-this-later'
CORS(app, origins=["https://souq-frontend.onrender.com", "http://localhost:3000"])
db.init_app(app)
JWTManager(app)

app.register_blueprint(auth_bp)
app.register_blueprint(products_bp)
app.register_blueprint(orders_bp)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)