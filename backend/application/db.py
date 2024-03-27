from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

class Role(db.Model,RoleMixin):
    __tablename__ = 'role'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255))

class User(db.Model,UserMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role',secondary='roles_users', backref=db.backref('users', lazy='joined'))
    section = db.relationship('Section', backref='creator')
    purchases = db.relationship('Purchase', backref='user', cascade="all, delete-orphan")
    shopping_cart = db.relationship('ShoppingCart', backref='user', cascade="all, delete-orphan")

class Section(db.Model):
    __tablename__ = 'section'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    active = db.Column(db.Boolean(), nullable=False)
    products = db.relationship('Product', backref='section', lazy='joined', cascade="all, delete-orphan")

class Product(db.Model):
    __tablename__ = 'product'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String)
    price = db.Column(db.Float)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    unit = db.Column(db.String(50))
    stock = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, nullable=True, default=db.func.current_timestamp())
    expired_at = db.Column(db.DateTime, nullable=True)
    shopping_cart = db.relationship('ShoppingCart', backref = 'product', cascade="all, delete-orphan" )

class ShoppingCart(db.Model):
    __tablename__ = 'shopping_cart'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)

class Purchase(db.Model):
    __tablename__ = 'purchase'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(50), nullable=False)  # Add a new column for common order ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    purchase_date = db.Column(db.DateTime, nullable=True)

    product = db.relationship('Product', backref='purchases')

class Approval(db.Model):
    __tablename__ = 'approval'

    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    status = db.Column(db.String(50), default="pending")
    description = db.Column(db.String, nullable=False)