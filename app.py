from flask import Flask, render_template, request, jsonify
import time

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
    
    # For now, we'll keep the placeholder response
    response = "This is a placeholder response from the character."
    
    return jsonify({
        'message': response,
        'typing': True
    })

if __name__ == '__main__':
    app.run(debug=True)
