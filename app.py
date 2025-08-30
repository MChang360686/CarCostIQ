from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# OpenAI configuration
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/analyze', methods=['POST'])
def analyze_prompt():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400
        
        # Call OpenAI to extract structured values
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """Extract structured values from the user's car insurance prompt. 
                    Return a JSON object with these fields:
                    - budget_range: string (e.g., "under_30k", "30k_50k", "50k_100k", "over_100k")
                    - family_size: integer (number of family members)
                    - commute_distance: string (e.g., "short", "medium", "long")
                    - climate_zone: string (e.g., "snowy", "hot", "moderate", "rainy")
                    - vehicle_type: string (e.g., "sedan", "suv", "truck", "compact")
                    - safety_priority: string (e.g., "high", "medium", "low")
                    - insurance_type: string (e.g., "comprehensive", "liability", "full_coverage")
                    - driving_history: string (e.g., "clean", "minor_violations", "major_violations")
                    - age_group: string (e.g., "young", "adult", "senior")
                    - location_type: string (e.g., "urban", "suburban", "rural")
                    
                    Only return the JSON object, no additional text."""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=500,
            temperature=0.1
        )
        
        # Extract the response content
        ai_response = response.choices[0].message.content
        
        # Try to parse the JSON response
        import json
        try:
            structured_values = json.loads(ai_response)
            return jsonify({
                'success': True,
                'structured_values': structured_values,
                'original_prompt': prompt
            })
        except json.JSONDecodeError:
            return jsonify({
                'success': False,
                'error': 'Failed to parse AI response',
                'ai_response': ai_response
            }), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        question = data.get('question', '')
        userId = data.get('userId', '')
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        print("\n" + "="*60)
        print("🚗 NEW CAR INSURANCE REQUEST RECEIVED")
        print("="*60)
        print(f"👤 User ID: {userId}")
        print(f"📝 Question: {question}")
        print("-"*60)
        
        # Call OpenAI to extract values in the exact format requested
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """Extract car shopping values from the user's prompt and return a JSON object in this EXACT format:
                    
                    {
                        "budget_min": integer (e.g., 15000, 25000, 35000),
                        "budget_max": integer (e.g., 25000, 35000, 50000),
                        "preferred_brands": array of strings (e.g., ["Toyota", "Honda", "Mazda"]),
                        "max_mileage": integer (e.g., 50000, 75000, 100000),
                        "min_year": integer (e.g., 2010, 2015, 2020),
                        "fuel_efficiency_importance": integer (1-5 scale, where 1=not important, 5=very important),
                        "maintenance_tolerance": string (e.g., "low", "medium", "high"),
                        "condition": string (e.g., "Excellent", "Good", "Fair"),
                        "state": string (e.g., "CA", "TX", "NY")
                    }
                    
                    Rules:
                    - If a value cannot be determined, use null
                    - For budget, extract min and max if given, otherwise use null
                    - For brands, create an array even if only one brand mentioned
                    - Use standard state abbreviations (CA, TX, NY, etc.)
                    - Only return the JSON object, no additional text"""
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            max_tokens=500,
            temperature=0.1
        )
        
        # Extract the response content
        ai_response = response.choices[0].message.content
        
        # Try to parse the JSON response and display in terminal
        import json
        try:
            structured_values = json.loads(ai_response)
            
            print("🔍 EXTRACTED VALUES IN REQUESTED FORMAT:")
            print("-"*60)
            print("💰 Budget Min: " + str(structured_values.get('budget_min', 'null')))
            print("💰 Budget Max: " + str(structured_values.get('budget_max', 'null')))
            print("🏷️  Preferred Brands: " + str(structured_values.get('preferred_brands', 'null')))
            print("🚗 Max Mileage: " + str(structured_values.get('max_mileage', 'null')))
            print("📅 Min Year: " + str(structured_values.get('min_year', 'null')))
            print("⛽ Fuel Efficiency Importance: " + str(structured_values.get('fuel_efficiency_importance', 'null')) + "/5")
            print("🔧 Maintenance Tolerance: " + str(structured_values.get('maintenance_tolerance', 'null')))
            print("✨ Condition: " + str(structured_values.get('condition', 'null')))
            print("🗺️  State: " + str(structured_values.get('state', 'null')))
            print("-"*60)
            print("✅ Values extracted in requested format!")
            print("="*60)
            print()
            
            # Return empty response to frontend (no display)
            return jsonify({'message': 'Values extracted in requested format and logged to terminal'})
            
        except json.JSONDecodeError:
            print(f"❌ Failed to parse AI response: {ai_response}")
            print("="*60)
            print()
            return jsonify({
                'error': 'Failed to parse AI response',
                'ai_response': ai_response
            }), 500
            
    except Exception as e:
        print(f"💥 Error occurred: {str(e)}")
        print("="*60)
        print()
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, port=8000)
