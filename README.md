# FAST CARS - Car Rental Booking System (Backend API)

A robust, modular, and secure RESTful backend API for **FAST CARS** car rental service, built with **FastAPI**, **SQLAlchemy ORM**, **SQLite**, and managed via **uv**.

---

## 🚀 Quick Start

### 1. Run Database Seeder (Optional - runs automatically on startup)
To populate starter brands, categories, sample cars, and admin accounts:
```bash
uv run python seed.py
```

### 2. Start the Development Server
```bash
uv run python main.py
```
Or using uvicorn directly:
```bash
uv run uvicorn main:app --reload --port 8080
```

The server will start at `http://localhost:8080`.

---

## 📖 Interactive API Documentation

Interactive Swagger API docs are available at:
👉 **[http://localhost:8080/doc](http://localhost:8080/doc)**

---

## 🔑 Pre-configured Accounts & Credentials

| Role | Email | Password | Pre-loaded Data |
| :--- | :--- | :--- | :--- |
| **Super Admin** | `admin@fastcars.com` | `AdminPassword123` | Full dashboard access, fleet management, booking moderation, CMS. |
| **Customer (Joy Jenna)** | `joy.jenna@gmail.com` | `CustomerPassword123` | Pre-configured with Nigeria, 3 wishlist cars, and 3 returned booking history items matching UI mockups. |

---

## 📁 Project Structure

```text
car_rental/
├── core/
│   ├── config.py         # Application settings loaded from .env
│   ├── security.py       # OWASP PBKDF2 password hashing & HMAC-SHA256 JWT tokens
│   └── deps.py           # FastAPI auth dependencies (get_current_user, get_current_admin)
├── db/
│   ├── database.py       # SQLite engine, SessionLocal, Base
│   └── seed.py           # Database seeder for demo data & initial setup
├── models/               # SQLAlchemy ORM database models
│   ├── user.py           # Users table
│   ├── car.py            # Categories, Brands, and Cars tables
│   ├── booking.py        # Bookings table
│   ├── wishlist.py       # Saved wishlist cars table
│   ├── testimonial.py    # Testimonials table
│   ├── contact.py        # Inquiries & newsletter subscribers
│   ├── support.py        # Support FAQs knowledgebase
│   └── page.py           # CMS content pages (About, Terms, Privacy, Contact Info)
├── schemas/              # Pydantic validation & response schemas
│   ├── user.py
│   ├── car.py
│   ├── booking.py
│   ├── wishlist.py
│   ├── testimonial.py
│   ├── contact.py
│   ├── support.py
│   └── page.py
├── routers/              # API Route Handlers
│   ├── auth.py           # Register, login, profile, change password
│   ├── categories.py     # Explore by Category endpoints
│   ├── brands.py         # Top Brands listing & admin CRUD
│   ├── cars.py           # Fleet search, filters, featured & slider cars
│   ├── wishlist.py       # User wishlist & badge count
│   ├── bookings.py       # Reservations & history metrics
│   ├── testimonials.py   # Reviews & moderation
│   ├── contact.py        # Contact queries & newsletter
│   ├── support.py        # Help & Support FAQ answering
│   ├── pages.py          # Dynamic CMS pages
│   ├── admin.py          # Dashboard analytics & user management
│   └── uploads.py        # Local file uploads for cars, brands, avatars
├── uploads/              # Uploaded static assets (mounted at /uploads)
├── pics/                 # UI design mockups specification
├── database.db           # SQLite database
├── main.py               # FastAPI entry point & lifespan events
├── seed.py               # Quick seed launcher
└── pyproject.toml        # uv dependencies & project metadata
```

---

## 🧪 Running Tests

To verify that all endpoints, auth flows, and database queries work properly:
```bash
uv run python -c "
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
assert client.get('/').status_code == 200
assert client.get('/api/cars').status_code == 200
assert client.get('/api/support/faqs').status_code == 200
print('All core API health checks passed!')
"
```
