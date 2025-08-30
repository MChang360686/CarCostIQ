import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()

class ValuesExtractor:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
    
    def extract_values(self, prompt):
        """
        Extract car shopping values from a prompt using OpenAI API in the exact format requested
        
        Args:
            prompt (str): User's text prompt describing their car shopping needs
            
        Returns:
            dict: Values extracted in the requested JSON format
        """
        try:
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
                        "content": prompt
                    }
                ],
                max_tokens=500,
                temperature=0.1
            )
            
            ai_response = response.choices[0].message.content
            
            # Parse the JSON response
            structured_values = json.loads(ai_response)
            
            return {
                'success': True,
                'structured_values': structured_values,
                'original_prompt': prompt
            }
            
        except json.JSONDecodeError as e:
            return {
                'success': False,
                'error': 'Failed to parse AI response',
                'ai_response': ai_response
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_available_fields(self):
        """
        Return the list of available fields that can be extracted
        
        Returns:
            list: Available field names
        """
        return [
            'budget_min',
            'budget_max', 
            'preferred_brands',
            'max_mileage',
            'min_year',
            'fuel_efficiency_importance',
            'maintenance_tolerance',
            'condition',
            'state'
        ]

# Example usage
if __name__ == "__main__":
    extractor = ValuesExtractor()
    
    # Test with a sample prompt
    test_prompt = "I'm looking for a Toyota or Honda sedan under $25k, preferably 2018 or newer with under 75k miles. Fuel efficiency is very important to me (5/5), and I have low maintenance tolerance. I want it in excellent condition and I'm shopping in California."
    
    result = extractor.extract_values(test_prompt)
    print("Extraction Result:")
    print(json.dumps(result, indent=2))
