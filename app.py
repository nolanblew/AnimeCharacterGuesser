from flask import Flask, render_template, request, jsonify
import time
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json['message']
    
    # Simulate "typing" delay
    time.sleep(2)
    
    # Generate a random number between 1 and 100 for the placeholder response
    random_number = random.randint(1, 100)
    response = f"Here's a random number between 1 and 100: {random_number}"
    
    return jsonify({
        'message': response,
        'typing': True
    })

if __name__ == '__main__':
    app.run(debug=True)
