import os
import sys
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import re
from pydantic import BaseModel, Field
from typing import List

# Ensure the root project directory is in the search path to support absolute imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from app.core.database import SessionLocal
from app.models.vehicle import Vehicle

# Load environment variables
load_dotenv()

# Define the Pydantic schemas for Structured Outputs
class VehicleAI(BaseModel):
    license_plate: str = Field(..., description="Exactly 7 or 8 digits. Only numbers (0-9). MUST be unique.")
    manufacturer: str = Field(..., description="Realistic car manufacturer.")
    model: str = Field(..., description="Realistic car model.")
    year: int = Field(..., description="Manufacturing year (between 2000 and 2026).")
    color: str = Field(..., description="Realistic standard car color.")

class VehicleList(BaseModel):
    vehicles: List[VehicleAI]

def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY environment variable is not set.")
        print("Please add GEMINI_API_KEY to your .env file.")
        sys.exit(1)

    # 1. Read prompt instructions from md file
    instructions_path = os.path.join(os.path.dirname(__file__), "llm_instructions.md")
    if not os.path.exists(instructions_path):
        print(f"ERROR: Instructions file not found at {instructions_path}")
        sys.exit(1)

    with open(instructions_path, "r", encoding="utf-8") as f:
        system_instructions = f.read()

    print("Connecting to Gemini API to generate vehicles...")
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        print("ERROR: google-genai library not found. Install it by running: pip install google-genai")
        sys.exit(1)

    # 2. Call Gemini model with structured output config
    client = genai.Client(api_key=api_key)
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Generate exactly 100 vehicles complying with the instructions.",
            config=types.GenerateContentConfig(
                system_instruction=system_instructions,
                response_mime_type="application/json",
                response_schema=VehicleList,
                temperature=0.7,
            )
        )
    except Exception as e:
        print(f"ERROR calling Gemini API: {e}")
        sys.exit(1)

    # 3. Parse output structure
    try:
        # Structured output returns parsed result on response.parsed or we can parse response.text
        vehicle_list: VehicleList = response.parsed
        if not vehicle_list or not vehicle_list.vehicles:
            print("ERROR: Received empty structure from Gemini.")
            sys.exit(1)
    except Exception as e:
        print(f"ERROR parsing structured JSON output: {e}")
        sys.exit(1)

    vehicles_to_load = vehicle_list.vehicles
    print(f"Gemini successfully generated {len(vehicles_to_load)} vehicles.")

    # 4. Insert into the database using SQLAlchemy
    db: Session = SessionLocal()
    success_count = 0
    skipped_format_count = 0
    skipped_duplicate_count = 0

    print("Beginning database load...")
    for idx, v_data in enumerate(vehicles_to_load, start=1):
        # Double check format validation: must be digits only and length 7 or 8
        if not re.match(r"^\d{7,8}$", v_data.license_plate):
            print(f"[{idx}/100] Skipping plate '{v_data.license_plate}' - invalid format (must be 7 or 8 digits).")
            skipped_format_count += 1
            continue

        # Check if the plate already exists in the database
        exists = db.query(Vehicle).filter(Vehicle.license_plate == v_data.license_plate).first()
        if exists:
            print(f"[{idx}/100] Skipping plate '{v_data.license_plate}' - already exists in the database.")
            skipped_duplicate_count += 1
            continue

        try:
            db_vehicle = Vehicle(
                license_plate=v_data.license_plate,
                manufacturer=v_data.manufacturer,
                model=v_data.model,
                year=v_data.year,
                color=v_data.color
            )
            db.add(db_vehicle)
            db.commit()
            success_count += 1
            print(f"[{idx}/100] Loaded: {v_data.manufacturer} {v_data.model} ({v_data.license_plate})")
        except IntegrityError:
            db.rollback()
            print(f"[{idx}/100] Skipped: Integrity error for plate {v_data.license_plate}.")
            skipped_duplicate_count += 1
        except Exception as e:
            db.rollback()
            print(f"[{idx}/100] Failed to load plate {v_data.license_plate}: {e}")

    db.close()

    print("\n--- Load Summary ---")
    print(f"Successfully loaded: {success_count} vehicles")
    print(f"Skipped (format invalid): {skipped_format_count} vehicles")
    print(f"Skipped (already exists): {skipped_duplicate_count} vehicles")
    print("--------------------")

if __name__ == "__main__":
    main()
