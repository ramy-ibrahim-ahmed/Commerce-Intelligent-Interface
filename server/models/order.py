from sqlalchemy import Column, Integer, DateTime, func
from ..core import ORM_BASE


class OrderModel(ORM_BASE):
    __tablename__ = "Orders"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    