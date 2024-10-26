import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_socketio import SocketIO
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

character = "jack"

generation_config = {
    "temperature": 0.5,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="you have to role play as witnesses in a murder mystery\nthe story is...",
)

@socketio.on('message')
def handle_message(data):
    user_input = data['message']
    chat_session = model.start_chat(history=[])
    
    # Use the dynamically set character in the message
    chat_session.send_message(f"act as {character} (don't reply to this message)")
    
    response = chat_session.send_message(user_input)
    model_response = response.text

    # Append to chat history
    chat_session.history.append({"role": "user", "parts": [user_input]})
    chat_session.history.append({"role": "model", "parts": [model_response]})

    # Send response back to the client
    socketio.emit('response', {'message': model_response})

@app.route('/interrogate')
def index():
    return render_template('index.html')

@app.route('/')
def witness_selection():
    return render_template('witness-selection.html')

@app.route('/submit', methods=['POST'])
def submit():
    global character
    character = request.form.get('character', 'jack')  # Default to 'jack' if not provided
    return redirect(url_for('index'))

if __name__ == '__main__':
    socketio.run(app, debug=True)
=======
import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_socketio import SocketIO
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

character = "jack"

generation_config = {
    "temperature": 0.5,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="you have to role play as witnesses in a murder mystery\nthe story is...",
)

@socketio.on('message')
def handle_message(data):
    user_input = data['message']
    chat_session = model.start_chat(history=[])
    
    # Use the dynamically set character in the message
    chat_session.send_message(f"act as {character} (don't reply to this message)")
    
    response = chat_session.send_message(user_input)
    model_response = response.text

    # Append to chat history
    chat_session.history.append({"role": "user", "parts": [user_input]})
    chat_session.history.append({"role": "model", "parts": [model_response]})

    # Send response back to the client
    socketio.emit('response', {'message': model_response})

@app.route('/interrogate')
def index():
    return render_template('index.html')

@app.route('/')
def witness_selection():
    return render_template('witness-selection.html')

@app.route('/submit', methods=['POST'])
def submit():
    global character
    character = request.form.get('character', 'jack')  # Default to 'jack' if not provided
    return redirect(url_for('index'))

if __name__ == '__main__':
    socketio.run(app, debug=True)
