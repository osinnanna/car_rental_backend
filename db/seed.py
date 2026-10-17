import os
from datetime import datetime, timedelta
from db.database import SessionLocal, create_tables
from models.user import User
from models.car import Category, Brand, Car
from models.wishlist import Wishlist
from models.booking import Booking
from models.page import Page
from models.testimonial import Testimonial
from models.support import FAQ
from core.security import hash_password


def seed_database():
    """Seed initial sample data to make the car rental application immediately functional."""
    # Ensure database tables exist
    create_tables()

    # Ensure upload directories exist
    for sub in ["cars", "brands", "avatars", "categories"]:
        os.makedirs(os.path.join("uploads", sub), exist_ok=True)

    db = SessionLocal()
    try:
        # 1. Admin User
        admin_email = "admin@fastcars.com"
        admin = db.query(User).filter(User.email == admin_email).first()
        if not admin:
            admin = User(
                email=admin_email,
                full_name="System Administrator",
                password_hash=hash_password("AdminPassword123"),
                phone_number="+1 800 555 0199",
                country="United States",
                is_admin=True,
            )
            db.add(admin)
            print("Seeded Admin: admin@fastcars.com / AdminPassword123")

        # 2. Demo Customer (Joy Jenna from UI mockups)
        customer_email = "joy.jenna@gmail.com"
        customer = db.query(User).filter(User.email == customer_email).first()
        if not customer:
            customer = User(
                email=customer_email,
                full_name="Joy Jenna",
                password_hash=hash_password("CustomerPassword123"),
                phone_number="+234 801 234 5678",
                country="Nigeria",
                avatar_url="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80",
                is_admin=False,
            )
            db.add(customer)
            print("Seeded Customer: joy.jenna@gmail.com / CustomerPassword123")

        db.commit()
        db.refresh(customer)

        # 3. Categories (from UI mockup: Explore by Category)
        categories_data = [
            {
                "name": "Fast Cars",
                "slug": "fast-cars",
                "description": "High speed. High thrills.",
                "image_url": "https://images.unsplash.com/photo-1617788138017-80ad40651399?auto=format&fit=crop&w=600&q=80",
            },
            {
                "name": "Sport Cars",
                "slug": "sport-cars",
                "description": "Performance meets style.",
                "image_url": "https://images.unsplash.com/photo-1544829099-b9a0c07fad1a?auto=format&fit=crop&w=600&q=80",
            },
            {
                "name": "Neutral Cars",
                "slug": "neutral-cars",
                "description": "Comfort & class.",
                "image_url": "https://images.unsplash.com/photo-1590362891991-f776e747a588?auto=format&fit=crop&w=600&q=80",
            },
        ]

        category_map = {}
        for cat in categories_data:
            existing = db.query(Category).filter(Category.slug == cat["slug"]).first()
            if not existing:
                existing = Category(**cat)
                db.add(existing)
                db.commit()
                db.refresh(existing)
            category_map[cat["slug"]] = existing

        # 4. Brands (from UI mockup: Top Brands)
        brands_data = [
            ("Mercedes-Benz", "https://www.car-logos.org/wp-content/uploads/2011/09/mercedes.png"),
            ("Honda", "https://www.car-logos.org/wp-content/uploads/2011/09/honda.png"),
            ("BMW", "https://www.car-logos.org/wp-content/uploads/2011/09/bmw.png"),
            ("Lamborghini", "https://www.car-logos.org/wp-content/uploads/2011/09/lamborghini.png"),
            ("Maserati", "https://www.car-logos.org/wp-content/uploads/2011/09/maserati.png"),
            ("Audi", "https://www.car-logos.org/wp-content/uploads/2011/09/audi.png"),
        ]

        brand_map = {}
        for name, logo in brands_data:
            existing = db.query(Brand).filter(Brand.name == name).first()
            if not existing:
                existing = Brand(name=name, logo_url=logo)
                db.add(existing)
                db.commit()
                db.refresh(existing)
            brand_map[name] = existing

        # 5. Cars (matching the mockups: Mercedes C63, Lamborghini Huracan, Honda Civic, BMW M4, etc.)
        cars_data = [
            {
                "brand_id": brand_map["Mercedes-Benz"].id,
                "category_id": category_map["sport-cars"].id,
                "title": "Mercedes-Benz C63",
                "overview": "Twin-turbo V8 engine delivering high performance with luxury comfort.",
                "price_per_day": 120.0,
                "fuel_type": "Petrol",
                "model_year": 2024,
                "seating_capacity": 5,
                "transmission": "Automatic",
                "image_url": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&w=800&q=80",
                "is_featured": True,
                "is_slider": True,
                "air_conditioner": True,
                "power_steering": True,
                "anti_lock_braking": True,
                "leather_seats": True,
                "power_windows": True,
                "driver_airbag": True,
                "passenger_airbag": True,
            },
            {
                "brand_id": brand_map["Lamborghini"].id,
                "category_id": category_map["fast-cars"].id,
                "title": "Lamborghini Huracán",
                "overview": "Naturally aspirated V10 supercar engineered to thrill at top speeds.",
                "price_per_day": 450.0,
                "fuel_type": "Petrol",
                "model_year": 2024,
                "seating_capacity": 2,
                "transmission": "Automatic",
                "image_url": "https://images.unsplash.com/photo-1544829099-b9a0c07fad1a?auto=format&fit=crop&w=800&q=80",
                "is_featured": True,
                "is_slider": True,
                "air_conditioner": True,
                "power_steering": True,
                "anti_lock_braking": True,
                "leather_seats": True,
                "driver_airbag": True,
                "passenger_airbag": True,
            },
            {
                "brand_id": brand_map["Honda"].id,
                "category_id": category_map["neutral-cars"].id,
                "title": "Honda Civic",
                "overview": "Reliable, fuel-efficient compact sedan built for everyday comfort.",
                "price_per_day": 80.0,
                "fuel_type": "Petrol",
                "model_year": 2023,
                "seating_capacity": 5,
                "transmission": "Manual",
                "image_url": "https://images.unsplash.com/photo-1590362891991-f776e747a588?auto=format&fit=crop&w=800&q=80",
                "is_featured": True,
                "is_slider": False,
                "air_conditioner": True,
                "power_steering": True,
                "anti_lock_braking": True,
                "driver_airbag": True,
                "power_windows": True,
            },
            {
                "brand_id": brand_map["BMW"].id,
                "category_id": category_map["sport-cars"].id,
                "title": "BMW M4",
                "overview": "Pure driving dynamics, aggressive styling, and track-proven agility.",
                "price_per_day": 150.0,
                "fuel_type": "Petrol",
                "model_year": 2024,
                "seating_capacity": 4,
                "transmission": "Automatic",
                "image_url": "https://images.unsplash.com/photo-1555215695-3004980ad54e?auto=format&fit=crop&w=800&q=80",
                "is_featured": False,
                "is_slider": False,
                "air_conditioner": True,
                "power_steering": True,
                "anti_lock_braking": True,
                "leather_seats": True,
                "driver_airbag": True,
            },
            {
                "brand_id": brand_map["Audi"].id,
                "category_id": category_map["sport-cars"].id,
                "title": "Audi RS7",
                "overview": "Four-door coupe with executive prestige and heart-pounding acceleration.",
                "price_per_day": 180.0,
                "fuel_type": "Petrol",
                "model_year": 2024,
                "seating_capacity": 5,
                "transmission": "Automatic",
                "image_url": "https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?auto=format&fit=crop&w=800&q=80",
                "is_featured": False,
                "is_slider": False,
                "air_conditioner": True,
                "power_steering": True,
                "anti_lock_braking": True,
                "leather_seats": True,
            },
            {
                "brand_id": brand_map["Maserati"].id,
                "category_id": category_map["fast-cars"].id,
                "title": "Maserati Ghibli",
                "overview": "Italian craftsmanship meets twin-turbocharged racing heritage.",
                "price_per_day": 220.0,
                "fuel_type": "Petrol",
                "model_year": 2024,
                "seating_capacity": 5,
                "transmission": "Automatic",
                "image_url": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=800&q=80",
                "is_featured": False,
                "is_slider": False,
                "air_conditioner": True,
                "power_steering": True,
                "anti_lock_braking": True,
                "leather_seats": True,
            },
        ]

        car_map = {}
        for c in cars_data:
            existing = db.query(Car).filter(Car.title == c["title"]).first()
            if not existing:
                existing = Car(**c)
                db.add(existing)
                db.commit()
                db.refresh(existing)
            car_map[c["title"]] = existing

        # 6. Wishlist for Joy Jenna (Lamborghini Huracan, Mercedes-Benz C63, BMW M4)
        saved_cars = ["Lamborghini Huracán", "Mercedes-Benz C63", "BMW M4"]
        for title in saved_cars:
            if title in car_map:
                car = car_map[title]
                w = db.query(Wishlist).filter(Wishlist.user_id == customer.id, Wishlist.car_id == car.id).first()
                if not w:
                    db.add(Wishlist(user_id=customer.id, car_id=car.id))
        db.commit()

        # 7. Booking History for Joy Jenna (Returned rentals matching mockups)
        history_bookings = [
            (car_map["Mercedes-Benz C63"], datetime(2025, 4, 12), datetime(2025, 4, 15), "Returned", 360.0),
            (car_map["Lamborghini Huracán"], datetime(2025, 4, 3), datetime(2025, 4, 5), "Returned", 900.0),
            (car_map["Honda Civic"], datetime(2025, 3, 20), datetime(2025, 3, 25), "Returned", 400.0),
        ]
        for car, f_date, t_date, b_status, cost in history_bookings:
            existing = db.query(Booking).filter(
                Booking.user_id == customer.id,
                Booking.car_id == car.id,
                Booking.from_date == f_date,
            ).first()
            if not existing:
                db.add(Booking(
                    user_id=customer.id,
                    car_id=car.id,
                    from_date=f_date,
                    to_date=t_date,
                    total_cost=cost,
                    status=b_status,
                    message="Great experience with FAST CARS!",
                ))
        db.commit()

        # 8. CMS Pages
        pages_data = [
            {
                "page_type": "aboutus",
                "title": "About FAST CARS",
                "content": "FAST CARS is a premier car rental service offering an extensive fleet of luxury, sport, and everyday vehicles at competitive rates.",
            },
            {
                "page_type": "terms",
                "title": "Terms and Conditions",
                "content": "All renters must hold a valid driver's license and be at least 21 years of age. Insurance coverage is included with every rental.",
            },
            {
                "page_type": "privacy",
                "title": "Privacy Policy",
                "content": "We value your privacy and safeguard all user data in accordance with international data protection standards.",
            },
            {
                "page_type": "contactinfo",
                "title": "Contact Information",
                "content": "Address: 124 Marina Boulevard, Victoria Island, Lagos, Nigeria. Phone: +234 800 FAST CARS. Email: support@fastcars.com",
            },
        ]
        for p in pages_data:
            existing = db.query(Page).filter(Page.page_type == p["page_type"]).first()
            if not existing:
                db.add(Page(**p))
        db.commit()

        # 9. Initial Testimonials
        if db.query(Testimonial).count() == 0:
            db.add(Testimonial(
                user_id=customer.id,
                content="Booking the Mercedes C63 was completely frictionless. Clean car, fast pickup, highly recommended!",
                status="Active",
            ))
            db.commit()

        # 10. Support FAQs (matching UI Help & Support page)
        faqs_data = [
            {
                "question": "How do I check my booking?",
                "answer": "You can view all your active and past reservations under the 'Booking History' tab in the navigation menu, with full details and rental status.",
                "category": "Booking",
            },
            {
                "question": "How do I modify or cancel my reservation?",
                "answer": "To cancel or modify a reservation, go to 'Booking History', select your booking, and click 'Cancel Booking', or reach out to our team at support@fastcars.com.",
                "category": "Booking",
            },
            {
                "question": "What cars are currently available for rental?",
                "answer": "All available cars can be browsed on the 'Browse Cars' page or explored by category (Fast Cars, Sport Cars, Neutral Cars) on our homepage.",
                "category": "Fleet",
            },
            {
                "question": "What are the requirements to rent a car?",
                "answer": "Renters must be at least 21 years old, have a valid driver's license held for at least one year, and present a valid government-issued ID.",
                "category": "Requirements",
            },
            {
                "question": "What payment methods are supported?",
                "answer": "We accept major debit and credit cards (Visa, MasterCard, Verve) as well as secure online bank transfers.",
                "category": "General",
            },
            {
                "question": "What happens if I return the car late?",
                "answer": "A grace period of 1 hour is provided. Returns exceeding 1 hour may incur an additional day's rental charge.",
                "category": "General",
            },
        ]
        for f in faqs_data:
            existing = db.query(FAQ).filter(FAQ.question == f["question"]).first()
            if not existing:
                db.add(FAQ(**f))
        db.commit()

        print("Database seeded successfully with all categories, brands, cars, wishlist, pages, and FAQs!")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
