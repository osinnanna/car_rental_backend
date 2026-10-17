import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from core.config import settings
from db.database import create_tables
from db.seed import seed_database
from routers import (
    auth,
    categories,
    brands,
    cars,
    wishlist,
    bookings,
    testimonials,
    contact,
    support,
    pages,
    admin,
    uploads,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ensure database tables and starter seed data exist on startup."""
    create_tables()
    try:
        seed_database()
    except Exception as e:
        print(f"Startup seeder notice: {e}")
    yield


app = FastAPI(
    title="FAST CARS - Car Rental API",
    description="Comprehensive backend API for FAST CARS rental booking system.",
    version="1.0.0",
    docs_url="/doc",
    lifespan=lifespan,
)

# CORS configuration
origins = settings.ALLOWED_ORIGINS if settings.ALLOWED_ORIGINS else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static file serving for uploads (cars, brands, avatars)
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Register all API endpoints
prefix = settings.API_PREFIX
app.include_router(auth.router, prefix=prefix)
app.include_router(categories.router, prefix=prefix)
app.include_router(brands.router, prefix=prefix)
app.include_router(cars.router, prefix=prefix)
app.include_router(wishlist.router, prefix=prefix)
app.include_router(bookings.router, prefix=prefix)
app.include_router(testimonials.router, prefix=prefix)
app.include_router(contact.router, prefix=prefix)
app.include_router(support.router, prefix=prefix)
app.include_router(pages.router, prefix=prefix)
app.include_router(admin.router, prefix=prefix)
app.include_router(uploads.router, prefix=prefix)


@app.get("/", tags=["Health Check"])
def root():
    return {
        "status": "online",
        "service": "FAST CARS Rental API",
        "version": "1.0.0",
        "docs": "/doc",
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=settings.DEBUG)
