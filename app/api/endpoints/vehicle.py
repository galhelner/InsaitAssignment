from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import logging
import re

from app.core.database import SessionLocal
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleRequest, VehicleResponse, VehicleData

logger = logging.getLogger(__name__)

router = APIRouter()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/vehicle-info",
    response_model=VehicleResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Vehicle Info",
    description="Retrieve details of a vehicle by its license plate."
)
def get_vehicle_info(
    request: VehicleRequest,
    db: Session = Depends(get_db)
):
    try:
        # 1. Format validation: check if license plate contains only numbers and is 7 or 8 characters long
        if not re.match(r"^\d{7,8}$", request.license_plate):
            logger.info(f"Invalid license plate format: '{request.license_plate}'")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "error": "Invalid license plate format. Must be only numbers and 7 or 8 digits long."
                }
            )

        # 2. Database query
        db_vehicle = db.query(Vehicle).filter(
            Vehicle.license_plate == request.license_plate
        ).first()

        # 3. Vehicle not found (404)
        if not db_vehicle:
            logger.info(f"Vehicle with license plate {request.license_plate} not found.")
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "error": "Vehicle not found"
                }
            )

        # 4. Success (200)
        logger.info(f"Vehicle with license plate {request.license_plate} successfully retrieved.")
        return VehicleResponse(
            success=True,
            data=VehicleData.model_validate(db_vehicle)
        )

    except Exception as e:
        logger.error(f"Error querying vehicle info: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": f"Internal database or server error: {str(e)}"
            }
        )
