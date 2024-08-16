import os
from openai import OpenAI
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Set up the OpenAI API client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_character_response(user_message, anime_name, character_name, conversation_history, anime_description, character_description):
    try:
        # Prepare the messages for the API call
        messages = [
            {"role": "system", "content": f"""You are a character from the anime '{anime_name}'. Your name is {character_name}. 

To help you recall, here is the anime description: '{anime_description}'

Your character description: '{character_description}'

You will be texting back and forth with the user. The user is trying to guess your name from the conversation, but you don't need to worry about that too much. Do not reveal your identity unless the user specifically asks or correctly guesses your identity. You ARE the character, so act as the character would with the limited knowledge they might have in their perspective. ALWAYS remain as this character and do NOT stray. Do not offer to give the user hints. However, you can offer hints if the user asks. Be sure to provide detailed responses and that your responses can be distinguished from other characters from '{anime_name}'. Just answer the question and don't ask the user any follow-up questions unless you think it's important.

Please don't make up information, if you don't know it just say you don't know. Otherwise be very specific and respond to the user's questions as if you were the character, especially if the user asks about the character's backstory, personality, or relationships.

Provide your response in JSON format."""}
        ]
        
        # Add the conversation history
        messages.extend(conversation_history)
        
        # Add the latest user message
        messages.append({"role": "user", "content": user_message})
        
        response = client.chat.completions.create(
            model="gpt-4o-2024-08-06",  # Use an available model, adjust as needed
            messages=messages,
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
