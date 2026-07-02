from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

# Request body schema
class VehicleRequest(BaseModel):
    license_plate: str = Field(..., description="The license plate of the vehicle")

# Schema representing the database model data
class VehicleData(BaseModel):
    license_plate: str
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    color: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

# Response schema
class VehicleResponse(BaseModel):
    success: bool
    data: Optional[VehicleData] = None
    error: Optional[str] = None
