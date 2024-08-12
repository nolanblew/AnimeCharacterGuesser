import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up the OpenAI API client
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_character_response(user_message, anime_name, character_name):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are a character from the anime '{anime_name}'. Your name is {character_name}. Respond to the user's messages in character, without revealing your identity directly."},
                {"role": "user", "content": user_message}
            ],
            response_format={
                "type": "json_object",
                "schema": {
                    "type": "object",
                    "properties": {
                        "anime_name": {"type": "string"},
                        "character_name": {"type": "string"},
                        "correct_guess": {"type": "boolean"},
                        "response": {"type": "string"}
                    },
                    "required": ["anime_name", "character_name", "correct_guess", "response"]
                }
            }
        )
        
        return response.choices[0].message['content']
    except Exception as e:
        print(f"Error in API call: {e}")
        return None
