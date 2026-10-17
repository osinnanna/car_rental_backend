from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


# Category Schemas (Explore by Category)
class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    image_url: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Brand Schemas (Top Brands)
class BrandBase(BaseModel):
    name: str
    logo_url: Optional[str] = None


class BrandCreate(BrandBase):
    pass


class BrandUpdate(BaseModel):
    name: Optional[str] = None
    logo_url: Optional[str] = None


class BrandResponse(BrandBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Car Schemas
class CarBase(BaseModel):
    brand_id: int
    category_id: Optional[int] = None
    title: str
    overview: Optional[str] = None
    price_per_day: float
    fuel_type: str
    model_year: int
    seating_capacity: int
    transmission: str = "Automatic"
    image_url: Optional[str] = None

    # Showcase Flags
    is_featured: bool = False
    is_slider: bool = False

    # Vehicle Features / Accessories
    air_conditioner: bool = False
    power_door_locks: bool = False
    anti_lock_braking: bool = False
    brake_assist: bool = False
    power_steering: bool = False
    driver_airbag: bool = False
    passenger_airbag: bool = False
    power_windows: bool = False
    cd_player: bool = False
    central_locking: bool = False
    crash_sensor: bool = False
    leather_seats: bool = False
    is_available: bool = True


class CarCreate(CarBase):
    pass


class CarUpdate(BaseModel):
    brand_id: Optional[int] = None
    category_id: Optional[int] = None
    title: Optional[str] = None
    overview: Optional[str] = None
    price_per_day: Optional[float] = None
    fuel_type: Optional[str] = None
    model_year: Optional[int] = None
    seating_capacity: Optional[int] = None
    transmission: Optional[str] = None
    image_url: Optional[str] = None

    is_featured: Optional[bool] = None
    is_slider: Optional[bool] = None

    air_conditioner: Optional[bool] = None
    power_door_locks: Optional[bool] = None
    anti_lock_braking: Optional[bool] = None
    brake_assist: Optional[bool] = None
    power_steering: Optional[bool] = None
    driver_airbag: Optional[bool] = None
    passenger_airbag: Optional[bool] = None
    power_windows: Optional[bool] = None
    cd_player: Optional[bool] = None
    central_locking: Optional[bool] = None
    crash_sensor: Optional[bool] = None
    leather_seats: Optional[bool] = None
    is_available: Optional[bool] = None


class CarResponse(CarBase):
    id: int
    created_at: datetime
    updated_at: datetime
    brand: Optional[BrandResponse] = None
    category: Optional[CategoryResponse] = None

    model_config = ConfigDict(from_attributes=True)
