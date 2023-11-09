from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata = metadata)

class Role(db.Model, SerializerMixin):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    
    
    #Relationships
    users = db.relationship("User", back_populates = 'roles')

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    ph_address= db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.Integer, nullable=False)
    city_town = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Integer, nullable=False)
    
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    #relationship
    invoice = db.relationship('Invoice', back_populates = 'users')
    roles = db.relationship('Role', back_populates = 'users')

class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key = True)
    image = db.Column(db.String(255), nullable=False)
    p_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    category = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable = False)
    brand = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    #relationships
    categories = db.relationship('Category', back_populates = 'product')
    brands = db.relationship('Brand', back_populates = 'product')
    invoice = db.relationship('Invoice', back_populates = 'products')
    invoice_products = db.relationship('InvoiceProducts', back_populates = 'product_rl')
   
class Category (db.Model, SerializerMixin):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key = True)
    cat_name = db.Column(db.String(150), nullable =False)
    
    #relationships
    product = db.relationship('Product', back_populates = 'categories')
    
class Brand (db.Model, SerializerMixin):
    __tablename__ = 'brands'
    
    id = db.Column(db.Integer, primary_key = True)
    brand_name = db.Column(db.String(150), nullable =False)
    brand_logo = db.Column(db.String(255), nullable =False)
    
    #relationships 
    product = db.relationship('Product', back_populates = 'brands')
    
class Invoice (db.Model, SerializerMixin):
    __tablename__ = 'invoices'
    
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    cost = db.Column(db.Integer, nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.now)
    
    #relationships
    users = db.relationship('User', back_populates = 'invoice')
    products = db.relationship('Product', back_populates = 'invoice')
    invoice_products = db.relationship('InvoiceProducts', back_populates = 'invoice_rl')
    

class InvoiceProducts(db.Model, SerializerMixin):
    __tablename__ = 'invoice_products'
    id = db.Column(db.Integer, primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable = False)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    #relationships 
    product_rl = db.relationship('Product', back_populates = 'invoice_products')
    invoice_rl = db.relationship('Invoice', back_populates = 'invoice_products')