from sqlalchemy import Column, String, BigInteger
from app.core.database import Base

class Vehicle(Base):
    __tablename__ = "Vehicle"

    license_plate = Column(String, primary_key=True, index=True)
    manufacturer = Column(String, nullable=True)
    model = Column(String, nullable=True)
    year = Column(BigInteger, nullable=True)
    color = Column(String, nullable=True)
