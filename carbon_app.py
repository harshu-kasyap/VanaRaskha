from flask import Flask, request, jsonify

app = Flask(__name__)

# Define emission factors (example values, replace with accurate data)
EMISSION_FACTORS = {
    "India": {
        "Transportation": 0.14,
        "Electricity": 0.82,
        "Diet": 1.25,
        "Waste": 0.1
    },
    "United States": {
        "Transportation": 0.12,
        "Electricity": 0.65,
        "Diet": 1.3,
        "Waste": 0.09
    },
    "United Kingdom": {
        "Transportation": 0.11,
        "Electricity": 0.45,
        "Diet": 1.2,
        "Waste": 0.08
    },
    "Canada": {
        "Transportation": 0.12,
        "Electricity": 0.5,
        "Diet": 1.3,
        "Waste": 0.09
    },
    "Australia": {
        "Transportation": 0.13,
        "Electricity": 0.6,
        "Diet": 1.3,
        "Waste": 0.09
    }
}

@app.route('/calculate_emission', methods=['POST'])
def calculate_emission():
    data = request.json
    country = data.get("country")
    distance = data.get("distance", 0) * 365
    electricity = data.get("electricity", 0) * 12
    meals = data.get("meals", 0) * 365
    waste = data.get("waste", 0) * 52

    # Validate country
    if country not in EMISSION_FACTORS:
        return jsonify({"error": "Invalid country selected"}), 400
    
    factors = EMISSION_FACTORS[country]

    transportation_emissions = factors["Transportation"] * distance
    energy_emissions = factors["Electricity"] * electricity
    food_emissions = factors["Diet"] * meals
    waste_emissions = factors["Waste"] * waste

    total_emissions = round((transportation_emissions + energy_emissions + food_emissions + waste_emissions) / 1000, 2)

    return jsonify({
        "transportation_emissions": round(transportation_emissions / 1000, 2),
        "energy_emissions": round(energy_emissions / 1000, 2),
        "food_emissions": round(food_emissions / 1000, 2),
        "waste_emissions": round(waste_emissions / 1000, 2),
        "total_emissions": total_emissions
    })

if __name__ == '__main__':
    app.run(debug=True)
