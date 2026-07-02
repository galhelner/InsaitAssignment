from fastapi import FastAPI
import logging

from app.api.endpoints.vehicle import router as vehicle_router

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Insait Assignment: Vehicle Info API",
    description="A FastAPI server to retrieve vehicle information from Supabase database.",
    version="1.0.0"
)

# Include the vehicle router
app.include_router(vehicle_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
