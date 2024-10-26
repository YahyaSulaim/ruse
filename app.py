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
  system_instruction="you have to role play as witnesses in a murder mystery\nthe story is\n\nIt was a crisp autumn evening when Clara Thompson, a beloved local café owner, decided to host a small gathering for her closest friends at her café, *Clara’s Corner*. The café, adorned with twinkling fairy lights and the aroma of freshly brewed coffee, was a haven in the community. Clara, warm-hearted and always the life of the party, wanted to celebrate her recent engagement to Jack Dawson, a local mechanic with whom she had built a loving relationship.\nHowever, beneath the surface of happiness, tensions simmered. Clara’s best friend, *Lily Carter, had secretly harbored feelings for Jack. Over the years, Clara had confided in Lily about her struggles, but the announcement of her engagement felt like a betrayal to Lily. Meanwhile, Clara's estranged sister, **Emma Grant*, resented Clara for inheriting the family home after their parents' passing, leading to a bitter divide between the sisters. \nAs the evening progressed, laughter filled the air, but little did they know that it would be their last gathering together.\n\nThe café was filled with close friends as Clara welcomed everyone with her trademark smile. Jack arrived early to help set up, but he was visibly anxious, burdened by financial troubles that had begun to weigh heavily on him. The guests mingled, sipping on their favorite brews, and Clara moved around, making sure everyone felt at home.\n\nUnbeknownst to Clara, Emma watched the evening unfold with jealousy and resentment, still grappling with the bitterness of their estrangement. Lily, on the other hand, was increasingly agitated, glancing at Jack when she thought no one was looking. Clara, unaware of the growing tension, poured herself a cup of her favorite coffee mix.\n\nThe gathering continued, but when Clara excused herself to the restroom, she unknowingly walked into the prelude of her demise. While the café buzzed with laughter, Lily seized the moment, slipping a tiny vial of cyanide into Clara's coffee cup, a malicious act masked under layers of betrayal and jealousy.\n\nAs the night progressed, Clara returned, blissfully unaware of the danger lurking in her drink. She raised her cup to toast her engagement, a moment captured forever in the hearts of her friends, unaware that it would soon turn into a grim memory.\n\nThe laughter and joy quickly turned to horror as Clara suddenly collapsed, clutching her chest. Jack rushed to her side, but it was too late; Clara was gone, poisoned by the very drink she cherished. The café was engulfed in panic, the festive atmosphere shattered in an instant.\n\nDetective Mark Lewis was soon called to the scene. Upon arrival, he observed the chaos, noting the distressed guests and the half-empty coffee cup on the table. The CCTV footage revealed no suspicious activity, yet it showed everyone entering and leaving, raising questions about what transpired in the café's confines.\n\nAs Detective Mark began his investigation, he interrogated each character, piecing together the events leading up to Clara’s death. \n\n- *Jack* claimed he arrived late, but the footage showed him entering the café earlier than he admitted. \n- *Emma* expressed bitterness towards Clara, revealing a simmering resentment yet insisting she hadn’t been there that night. \n- *Lily*, visibly shaken, provided an inconsistent timeline about her whereabouts.\n\nThe detective focused on Clara's coffee cup, discovering traces of cyanide. Text messages from Lily revealed her knowledge of Clara's favorite drink, suggesting a more sinister motive hidden beneath her facade of friendship.\n\n--\nthe truth: Lily’s jealousy and emotional turmoil over Clara's relationship with Jack drove her to an unthinkable act. The final piece of evidence—a discarded coffee cup from Lily’s hand—revealed the poison. Confronted with the evidence, Lily broke down, confessing her actions driven by betrayal.\n\nact like witnesses as youre asked to",
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
def interrogate():
    return render_template('chat.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/selectwictness')
def witness_selection():
    return render_template('witness-selection.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/crimescene')
def crime():
    return render_template('crime.html')

@app.route('/suspect')
def sus():
    return render_template('witness.html')


@app.route('/submit', methods=['POST'])
def submit():
    global character
    character = request.form.get('character', 'jack')  # Default to 'jack' if not provided
    return redirect(url_for('interrogate'))

if __name__ == '__main__':
    socketio.run(app, debug=True)