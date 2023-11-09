from app import app, db
from faker import Faker
from models import User, Product, Brand, Category, Invoice, InvoiceProducts, Invoice, Role
from datetime import datetime
from sqlalchemy.orm import sessionmaker
import random

fake = Faker()

with app.app_context():
    db.create_all()
    def delete_data():
        # this deletes existing db data in columns 
        print("🦸 Delete_data...")
        User.query.delete()
        Product.query.delete()
        Category.query.delete()
        Brand.query.delete()
        Invoice.query.delete()
        InvoiceProducts.query.delete()
        Role.query.delete()
    
    def seed_data():
        print("🦸‍♀️ Seeding User Roles...")
        admin_role = Role(name='Admin')
        db.session.add(admin_role)

        client_role = Role(name='Client')
        db.session.add(client_role)

        print("🦸‍♀️ Seeding Users with Faker...")
        roles = [1] + [random.choice([2, 3, 4]) for _ in range(49)]

        for i in range(50):  # Generate 50 fake users
            user = User(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                username=fake.user_name(),
                email=fake.email(),
                ph_address=fake.address(),
                password=fake.password(),
                telephone=fake.phone_number(),
                city_town=fake.city(),
                role=roles[i]  
            )
            db.session.add(user)

        db.session.commit()

        print("🦸‍♀️ Seeding Brands with Faker...")
        for _ in range(50):  # Generate 2 fake brands
            brand = Brand(
                brand_name=fake.company(),
                brand_logo=fake.url()
            )
            db.session.add(brand)

        categories = ("skin", "face", "nails", "eyes", "hair")
        print("🦸‍♀️ Seeding Categories with Faker...")
        for _ in range(5):  # Generate 4 fake categories
                category_name = fake.unique.random_element(elements=categories)
                category = Category(cat_name=category_name)
                db.session.add(category)

        print("🦸‍♀️ Seeding Products with Faker...")
        product_1 = Product(image="https://images.pexels.com/photos/3373739/pexels-photo-3373739.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1", p_name="Huddah Lipstick - Red Velvet", description="High-quality red lipstick that provides a smooth and long-lasting finish. Perfect for any occasion.", price=200, quantity=30, category=1, brand=1)
        product_2 = Product(image="https://images.pexels.com/photos/5403543/pexels-photo-5403543.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1", p_name="Rihanna Mascara - Volume Boost", description="Achieve voluminous lashes with Rihanna's mascara. This mascara lifts, separates, and adds volume for a dramatic look.", price=100, category=1,quantity=50,  brand=2)
        product_3 = Product(image="https://images.pexels.com/photos/3685523/pexels-photo-3685523.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1", p_name="Urban Chic Eyeshadow Palette", description="Explore a variety of shades with this eyeshadow palette. From subtle neutrals to bold colors, create endless eye looks.", price=250, category=3, quantity=200 ,brand=1)
        product_4 = Product(image="https://images.pexels.com/photos/2661256/pexels-photo-2661256.jpeg?auto=compress&cs=tinysrgb&w=1600", p_name="Luxury Makeup Brush Set", description="Upgrade your makeup routine with this luxurious brush set. The soft bristles and ergonomic handles ensure a flawless application.", price=150, category=4,quantity=34,  brand=2)
        product_5 = Product(image="https://images.pexels.com/photos/6417915/pexels-photo-6417915.jpeg?auto=compress&cs=tinysrgb&w=1600", p_name="Maybelline Lip Gloss - Pink Delight", description="Shiny and moisturizing lip gloss by Maybelline. Add a pop of color and shine to your lips with this Pink Delight shade.", price=120, category=1,quantity=70,  brand=3)
        product_6 = Product(image="https://images.pexels.com/photos/5849420/pexels-photo-5849420.jpeg?auto=compress&cs=tinysrgb&w=1600", p_name="MAC Blush Brush", description="Sculpt and define your cheeks with this MAC blush brush. Soft and angled bristles make application easy and precise.", price=50, category=4,quantity=390 , brand=4)
        product_7 = Product(image="https://images.pexels.com/photos/7797740/pexels-photo-7797740.jpeg?auto=compress&cs=tinysrgb&w=1600", p_name="Maybelline Lipstick - Coral Crush", description="Vibrant coral lipstick by Maybelline. Provides a creamy texture and bold color payoff.", price=180, category=1, quantity=100 , brand=3)
        product_8 = Product(image="https://images.pexels.com/photos/6476122/pexels-photo-6476122.jpeg?auto=compress&cs=tinysrgb&w=1600", p_name="MAC Foundation - Natural Glow", description="Lightweight foundation for a natural glow. Blends seamlessly and provides all-day coverage.", price=280, category=2,quantity=94,  brand=4)
        product_9 = Product(image="https://images.pexels.com/photos/3997378/pexels-photo-3997378.jpeg?auto=compress&cs=tinysrgb&w=1600", p_name="Rihanna Face Cream - Hydrating Moisture", description="Hydrating face cream by Rihanna. Infused with moisturizing ingredients for soft and supple skin.", price=220, category=2,quantity=60,  brand=2)
        product_10 = Product(image="https://images.pexels.com/photos/5871834/pexels-photo-5871834.jpeg?auto=compress&cs=tinysrgb&w=1600", p_name="MAC Concealer - Full Coverage", description="Full coverage concealer by MAC. Conceals imperfections and brightens the under-eye area.", price=150, category=2, quantity=20,  brand=4)
        product_11 = Product(image="https://images.pexels.com/photos/3115708/pexels-photo-3115708.jpeg?auto=compress&cs=tinysrgb&w=1600", p_name="Maybelline Eyeshadow Palette - Bold Hues", description="Dive into a world of bold hues with this Maybelline eyeshadow palette. Create vibrant and daring eye looks with a mix of matte and shimmer shades.", price=280, category=3,quantity=150,  brand=3)
        product_12 = Product(image="https://images.pexels.com/photos/279480/pexels-photo-279480.jpeg?auto=compress&cs=tinysrgb&w=1600", p_name="Huddah Makeup Brush Set", description="High-quality makeup brush set by Huddah Cosmetics. Includes brushes for eyes, face, and lips.", price=200, category=4,quantity=120,  brand=1)

        # Add products to the session and commit
        db.session.add_all([
            product_1, product_2, product_3, product_4, product_5, product_6, product_7, product_8, product_9, product_10, product_11, product_12
        ])
        db.session.commit()

        print("🦸‍♀️ Seeding Invoices with Faker...")
        for _ in range(50):  # Generate 3 fake invoices
            user = User.query.order_by(User.id).first()
            product = Product.query.order_by(Product.id).first()
            invoice = Invoice(
                users=user,
                products=product,
                quantity=fake.random_int(min=1, max=20),
                cost=fake.random_int(min=10, max=5000)
            )
            db.session.add(invoice)

        print("🦸‍♀️ Seeding Invoice_Products with Faker...")
        products = Product.query.all()
        invoices = Invoice.query.all()
        for _ in range(50):  # Generate 6 fake invoice products
            product = fake.random_element(products)
            invoice = fake.random_element(invoices)
            invoice_product = InvoiceProducts(
                product_rl=product,
                invoice_rl=invoice
            )
            db.session.add(invoice_product)

        db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        db.app = app  # Bind the app to the current SQLAlchemy instance
        delete_data()
        db.session.commit()
        seed_data()
        db.session.commit()
        
        print("🦸‍♀️ Done seeding!")
