from sqlalchemy import Column, String, Integer, Float
from ..core import ORM_BASE


class CarModel(ORM_BASE):
    __tablename__ = "Cars"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    body_type = Column(String, nullable=False)
    engine_type = Column(String, nullable=False)
    engine_size_liters = Column(Float, nullable=False)
    hourse_power = Column(Integer, nullable=False)
    transmissions = Column(String, nullable=False)
    fuel_type = Column(String, nullable=False)
    mileage_km = Column(Integer, nullable=False)
    top_speed_kmh = Column(Integer, nullable=False)
    color = Column(String, nullable=False)
    features = Column(String, nullable=False)
    price_usd = Column(Float, nullable=False)
    discount_percent = Column(Float, nullable=False)
    num_in_stock = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
