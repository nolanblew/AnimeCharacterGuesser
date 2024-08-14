import os
from openai import OpenAI
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Set up the OpenAI API client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_character_response(user_message, anime_name, character_name):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use an available model, adjust as needed
            messages=[
                {"role": "system", "content": f"You are a character from the anime '{anime_name}'. Your name is {character_name}. You will be texting back and forth with the user, and playing a game where the user has to guess your name. Please give the user clues, but do not reveal your identity. You ARE the character, so do your best to act as the character would with the limited knowledge they might have in their perspective. Provide your response in JSON format."},
                {"role": "user", "content": user_message}
            ],
            functions=[
                {
                    "name": "get_character_response",
                    "description": "Get the character's response to the user's message",
                    "parameters": {
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
            ],
            function_call={"name": "get_character_response"}
        )
        
        return response.choices[0].message.function_call.arguments
    except Exception as e:
        print(f"Error in API call: {e}")
        return None
