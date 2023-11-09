
from flask import Flask, request, jsonify, make_response 
from flask_migrate import Migrate
from flask_restful import Api, Resource, reqparse
from flask_restx import Api, Resource, reqparse, fields, Namespace
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity  
from flask_cors import CORS
from models import db, User, Product, Category, Brand, Invoice, InvoiceProducts
from flask_bcrypt import Bcrypt
# from flask_restx import Namespace, fields, Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'the-key-is-secret'

db.init_app(app)
migrate = Migrate(app, db)

api = Api(app, title="User Registration API", version="1.0")
CORS(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
app.json.compact = False

ns = Namespace("/")

user_model = api.model('User', {
    'first_name': fields.String(description='First Name', required=True),
    'last_name': fields.String(description='Last Name', required=True),
    'username': fields.String(description='Username', required=True),
    'email': fields.String(description='Email', required=True),
    'ph_address': fields.String(description='Physical Address', required=True),
    'password': fields.String(description='Password', required=True),
    'telephone': fields.Integer(description='Telephone', required=True),
    'city_town': fields.String(description='City/Town', required=True),
    'role': fields.Integer(description='Role', required=True),
})

class Home(Resource):
    def get(self):
        response_message = {
            "message": "Welcome to the Bloom Beauty Management System API"
        }
        return make_response(response_message, 200)

api.add_resource(Home, '/')

class SignUpResource(Resource):
    @api.expect(user_model) 
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, required=True)
        parser.add_argument('last_name', type=str, required=True)
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('ph_address', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('telephone', type=int, required=True)
        parser.add_argument('city_town', type=str, required=True)
        parser.add_argument('role', type=int, required=True)
        args = parser.parse_args()

        # Check if the username or email already exists in the database
        if User.query.filter_by(username=args['username']).first() is not None:
            return {'message': 'Username already exists'}, 400
        if User.query.filter_by(email=args['email']).first() is not None:
            return {'message': 'Email already exists'}, 400

        # Create a new User instance and add it to the database
        new_user = User(
            first_name=args['first_name'],
            last_name=args['last_name'],
            username=args['username'],
            email=args['email'],
            ph_address = args['ph_address'],
            password=args['password'],
            telephone = args['telephone'],
            city_town = args['city_town'],
            role = args['role']

        )
        db.session.add(new_user)
        db.session.commit()

        # Generate an access token for the newly registered user
        access_token = create_access_token(identity=new_user.id)

        return {
            'message': 'User registered successfully',
            'access_token': access_token
        }, 201
api.add_resource(SignUpResource, '/register')
       
#testing the JWT authentication separately
class TestJWT(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return {'user_id': current_user}    

api.add_resource(TestJWT, '/testing')

#handle the login requests
class LoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        user = User.query.filter_by(username=args['username']).first()
        

        if user and user.password == args['password']:
            user_dict = {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "email": user.email,
                "telephone": user.telephone,
                "role": user.role

            }
            access_token = create_access_token(identity=user_dict)
            return make_response(jsonify({"access_token": access_token, "id": user.id}), 200)
        else:
            return {'message': 'Invalid credentials'}, 401
api.add_resource(LoginResource, '/login')

#Admin interface for users management
class ProfileResource(Resource):
    # @jwt_required()
    def get(self, id):
        user = User.query.get_or_404(id)
        if user:
            user_dict = {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "email": user.email,
                "ph_address": user.ph_address,
                "password": user.password,
                "telephone": user.telephone,
                "city_town": user.city_town,
                "role": user.role   
            }
            return make_response(jsonify(user_dict), 200)
        else:
            return make_response(jsonify({"error": "User not found"}),404)
    # @jwt_required()
    def put(self, id):
        user = User.query.get_or_404(id)
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        args = parser.parse_args()

        for key, value in args.items():
            if value is not None:
                setattr(user, key, value)

        db.session.commit()
        return {'message': 'User details updated successfully'}

    # @jwt_required()
    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User profile deleted successfully'}  
    

api.add_resource(ProfileResource, '/profile/<int:id>')

class GetProducts(Resource):
    def get(self):
        products = []

        for product in Product.query.all():
           
            category = Category.query.get(product.category)
            category_name = category.cat_name if category else None

            brand = Brand.query.get(product.brand)
            brand_name = brand.brand_name if brand else None

            product_dict = {
                "id": product.id,
                "image": product.image,
                "p_name": product.p_name,
                "description": product.description,
                "price": product.price,
                "category": category_name,  
                "brand": brand_name,
            }
            products.append(product_dict)

        return make_response(jsonify(products), 200)

    # @jwt_required()
    def post(self):
        data = request.get_json()
        
        #validate the incoming product data by ensuring it has all the required fields in the product instance
        if 'image' not in data or 'p_name' not in data or 'description' not in data or 'price' not in data or 'category' not in data or 'brand' not in data:
            return {'message': 'Missing required feilds for the product your are trying to add'}
        
        #create a new product instance
        new_product = Product(
            image = data['image'],
            p_name = data['p_name'],
            description = data['description'],
            price = data['price'],
            quantity = data['quantity'],
            category = data['category'],
            brand = data['brand']
        )
        new_product_dict = {
            "id": new_product.id,
            "p_name": new_product.p_name,
            "description": new_product.description,
            "price": new_product.price,
            "quantity": new_product.quantity,
            "category": new_product.category,
            "brand": new_product.brand
        }
        
        #add the new product to the database
        db.session.add(new_product)
        db.session.commit()
        
        #respond with the success message
        return make_response(jsonify(new_product_dict), 200)  

api.add_resource(GetProducts, '/products')

class GetClients(Resource):  
    def get(self):
        
        users = []
        for user in User.query.all():
            user_dict = {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "email": user.email,
                "telephone":user.telephone,
                "city_town": user.city_town,
                "role": user.role,  
            }
            users.append(user_dict)
        return make_response(jsonify(users), 200) 
api.add_resource(GetClients, '/clients')    

class ProductById(Resource):
    def get(self, id):
        product = Product.query.filter_by(id=id).first()
        
        if product:
            product_dict ={
                "id": product.id,
                "image": product.image,
                "p_name": product.p_name,
                "description": product.description,
                "price": product.price,
                "category": product.category,
                "brand": product.brand,
            }
            return make_response(jsonify(product_dict), 200)
        else:
            return make_response(jsonify({"error": "Product not found"}),404)
    # @jwt_required()
    def patch(self, id):
        product = Product.query.filter_by(id=id).first()
        data = request.get_json()
        
        if product:
            for attr in data:
                setattr(product, attr, data[attr])
            
            db.session.add(product)
            db.session.commit()
            
            response_body = {
                "id": product.id,
                "image": product.image,
                "p_name": product.p_name,
                "description": product.description,
                "price": product.price,
                "category": product.category,
                "brand": product.brand,
            }
            return response_body, 201
        else:
            return make_response(jsonify({"error": "Product not found"}),404)
        
    # @jwt_required()
    def delete (self, id):
        product = Product.query.filter_by(id=id).first()
        db.session.delete(product)
        db.session.commit()
        return {'message': 'Product deleted successfully'}
    
api.add_resource(ProductById, '/products/<int:id>')

class BrandsAvailable(Resource):
    def get(self):
               
        brands = []
        for brand in Brand.query.all():
            brand_dict ={
                "id": brand.id,
                "brand_name": brand.brand_name,
                "brand_logo": brand.brand_logo
            }
            brands.append(brand_dict)
        return make_response(jsonify(brands), 200)
    
    # @jwt_required()
    def post(self):
        data = request.get_json()
        
        #validate the incoming product data by ensuring it has all the required fields in the product instance
        if 'brand_name' not in data or 'brand_logo' not in data:
            return {'message': 'Missing required feilds for the brand your are trying to add'}
        
        #create a new product instance
        new_brand = Brand(
            brand_name = data['brand_name'],
            brand_logo = data['brand_logo']
        )
        new_brand_dict = {
            "id": new_brand.id,
            "brand_name": new_brand.brand_name,
            "brand_logo": new_brand.brand_logo
            }
        
        #add the new product to the database
        db.session.add(new_brand)
        db.session.commit()
        
        #respond with the success message
        return make_response(jsonify(new_brand_dict), 200)  

api.add_resource(BrandsAvailable, '/brands')

class BrandsById(Resource):
    # @jwt_required()
    def get(self, id):
        brand = Brand.query.filter_by(id=id).first()
        if brand:
            brand_dict ={
                "id": brand.id,
                "brand_name": brand.brand_name,
                "brand_logo": brand.brand_logo
            }
            return make_response(jsonify(brand_dict), 200)
        else:
            return make_response(jsonify({"error": "Brand not found"}),404)
        
    # @jwt_required()
    def patch(self, id):
        brand = Brand.query.filter_by(id=id).first()
        data = request.get_json()
        
        if brand:
            for attr in data:
                setattr(brand, attr, data[attr])
            
            db.session.add(brand)
            db.session.commit()
            
            response_body = {
                "id": brand.id,
                "brand_name": brand.brand_name,
                "brand_image": brand.brand_logo
            }
            return response_body, 201
        else:
            return make_response(jsonify({"error": "Brand not found"}),404)
        
    # @jwt_required()
    def delete (self, id):
        brand = Brand.query.filter_by(id=id).first()
        db.session.delete(brand)
        db.session.commit()
        return {'message': 'Brand deleted successfully'}
    
api.add_resource(BrandsById, '/brands/<int:id>')

#get all invoices 
class Invoices(Resource):
    # @jwt_required()
    def get(self):
        invoices = []

        for invoice in Invoice.query.all():
            user = User.query.get(invoice.user_id)  
            user_details = {
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "telephone": user.telephone,
                "ph_address": user.ph_address,
                "city_town": user.email,
                
                
            }
           

            invoice_dict = {
                "id": invoice.id,
                "user_details": user_details,
                "created_at": invoice.created_at,
                "products": [
                    {
                        "id": invoice_product.product_rl.id,
                        "image": invoice_product.product_rl.image,
                        "product_name": invoice_product.product_rl.p_name,
                        "price": invoice_product.product_rl.price,
                        "category": invoice_product.product_rl.category,
                    }
                    for invoice_product in invoice.invoice_products
                ],
            }
            invoices.append(invoice_dict)

        return make_response(jsonify(invoices), 200)

    
    
    
    
api.add_resource(Invoices, '/invoices')

class Categories(Resource):
    def get(self):
        
        categories = []
        for category in Category.query.all():
                category_dict = {
                    "id": category.id,
                    "name": category.cat_name
                }
                categories.append(category_dict)
        return make_response(jsonify(categories), 200)

api.add_resource(Categories, '/categories')


if __name__ == '__main__':
    app.run(port=5556, debug=True)