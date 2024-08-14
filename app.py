from flask import Flask, render_template, request, jsonify, session
from openai_integration import get_character_response
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a real secret key

@app.route('/')
def index():
    return render_template('index.html')

from flask import redirect, url_for

@app.route('/chat')
def chat():
    if 'anime_name' not in session or 'character_name' not in session:
        # If the required session data is not present, redirect to the home page
        return redirect(url_for('index'))
    return render_template('chat.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    anime_name = request.json['anime_name']
    # For now, we'll use a placeholder character. In a real implementation,
    # you'd want to fetch a random character from the specified anime.
    character_name = "Taiga Aisaka"
    
    session['anime_name'] = anime_name
    session['character_name'] = character_name
    
    # Generate an initial greeting
    initial_greeting = get_character_response("Start the game with a greeting", anime_name, character_name)
    if initial_greeting:
        greeting_data = json.loads(initial_greeting)
        session['initial_greeting'] = greeting_data['response']
    else:
        session['initial_greeting'] = "Hello! I'm excited to play this game with you!"
    
    return jsonify({'success': True})

@app.route('/get_initial_greeting', methods=['GET'])
def get_initial_greeting():
    return jsonify({'message': session.get('initial_greeting', "Hello! I'm excited to play this game with you!")})

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json['message']
    anime_name = session.get('anime_name', 'Unknown Anime')
    character_name = session.get('character_name', 'Unknown Character')
    
    response_json = get_character_response(user_message, anime_name, character_name)
    
    if response_json:
        response_data = json.loads(response_json)
        return jsonify(response_data)
    else:
        return jsonify({
            'message': "I'm sorry, I couldn't process your message. Please try again.",
            'correct_guess': False,
            'anime_name': anime_name,
            'character_name': character_name
        })

if __name__ == '__main__':
    app.run(debug=True)
