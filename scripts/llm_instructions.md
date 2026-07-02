# Role & Task
You are an expert data generation AI. Your task is to generate exactly 100 realistic, unique vehicles for a database populate script.

# Output Requirements & Restrictions
You must generate a list of exactly 100 vehicles. Each vehicle must conform to the following specifications:

1. **`license_plate`**:
   - MUST contain **only numbers (digits 0-9)**. No letters, symbols, spaces, or dashes.
   - MUST be exactly **7 or 8 digits long**.
   - MUST be **completely unique** across all 100 generated vehicles.
   - MUST be highly randomized (e.g. `85647365`, `5492813`, `72048591`). Do NOT use sequential sequences (like `10000001`, `10000002`), simple counters, or predictable patterns.

2. **`manufacturer` & `model`**:
   - MUST be real, well-known car manufacturers and models.
   - Data should look reliable, clean, and professional.
   - Examples of acceptable manufacturers and models:
     - Toyota: Corolla, Camry, RAV4, Prius
     - Honda: Civic, Accord, CR-V, Pilot
     - Tesla: Model 3, Model Y, Model S, Model X
     - Hyundai: Elantra, Sonata, Tucson, Santa Fe
     - Ford: Mustang, Explorer, F-150, Escape
     - Chevrolet: Malibu, Equinox, Silverado, Bolt
     - BMW: 3 Series, 5 Series, X5, i4
     - Mercedes-Benz: C-Class, E-Class, GLC, EQE

3. **`year`**:
   - MUST be a realistic manufacturing year between **2000 and 2026** inclusive.

4. **`color`**:
   - MUST be a standard, realistic vehicle color (e.g., "White", "Black", "Silver", "Grey", "Blue", "Red", "Charcoal").

# Examples of Valid Data
Here are some examples of valid individual records:
- `{ "license_plate": "85647365", "manufacturer": "Toyota", "model": "Corolla", "year": 2021, "color": "Silver" }`
- `{ "license_plate": "5492813", "manufacturer": "Tesla", "model": "Model 3", "year": 2023, "color": "Black" }`
- `{ "license_plate": "72048591", "manufacturer": "Hyundai", "model": "Tucson", "year": 2022, "color": "Blue" }`
