from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from openai_integration import get_character_response
from anilist.anilist_api import fetch_anime_suggestions, fetch_characters
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a real secret key

@app.route('/')
def index():
    # Clear session variables when returning to the home page
    session.clear()
    return render_template('index.html')

@app.route('/chat')
def chat():
    if 'anime_name' not in session or 'character_name' not in session:
        # If the required session data is not present, redirect to the home page
        return redirect(url_for('index'))
    return render_template('chat.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    anime_name = request.json['anime_name']
    anime_id = request.json['anime_id']
    anime_description = request.json.get('anime_description', '')  # Use get() with a default value
    session['anime_name'] = anime_name
    session['anime_id'] = anime_id
    session['anime_description'] = anime_description
    return jsonify({'success': True})

@app.route('/select_character')
def select_character():
    anime_id = session.get('anime_id')
    if not anime_id:
        return redirect(url_for('index'))
    characters, anime_description = fetch_characters(anime_id)
    session['anime_description'] = anime_description
    return render_template('select_character.html', characters=characters)

@app.route('/set_character', methods=['POST'])
def set_character():
    character_name = request.json['character_name']
    character_description = request.json['character_description']
    session['character_name'] = character_name
    session['character_description'] = character_description
    session['conversation_history'] = []
    
    # Generate an initial greeting
    initial_greeting = get_character_response("Start the game with a greeting", session['anime_name'], character_name, [], session['anime_description'], character_description)
    if initial_greeting:
        greeting_data = json.loads(initial_greeting)
        session['initial_greeting'] = greeting_data['response']
        session['conversation_history'].append({"role": "assistant", "content": greeting_data['response']})
    else:
        session['initial_greeting'] = "Hello! I'm excited to play this game with you!"
        session['conversation_history'].append({"role": "assistant", "content": session['initial_greeting']})
    
    return jsonify({'success': True})

@app.route('/get_initial_greeting', methods=['GET'])
def get_initial_greeting():
    return jsonify({'message': session.get('initial_greeting', "Hello! I'm excited to play this game with you!")})

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json['message']
    anime_name = session.get('anime_name', 'Unknown Anime')
    character_name = session.get('character_name', 'Unknown Character')
    conversation_history = session.get('conversation_history', [])
    
    # Add user message to conversation history
    conversation_history.append({"role": "user", "content": user_message})
    
    response_json = get_character_response(user_message, anime_name, character_name, conversation_history)
    
    if response_json:
        response_data = json.loads(response_json)
        # Add assistant's response to conversation history
        conversation_history.append({"role": "assistant", "content": response_data['response']})
        session['conversation_history'] = conversation_history
        return jsonify(response_data)
    else:
        error_message = "I'm sorry, I couldn't process your message. Please try again."
        conversation_history.append({"role": "assistant", "content": error_message})
        session['conversation_history'] = conversation_history
        return jsonify({
            'message': error_message,
            'correct_guess': False,
            'anime_name': anime_name,
            'character_name': character_name
        })

@app.route('/search_anime', methods=['POST'])
def search_anime():
    search_term = request.json['search_term']
    app.logger.info(f"Searching for anime with term: {search_term}")
    anime_suggestions = fetch_anime_suggestions(search_term)
    app.logger.info(f"Received {len(anime_suggestions)} suggestions")
    return jsonify(anime_suggestions)

if __name__ == '__main__':
    app.run(debug=True)
