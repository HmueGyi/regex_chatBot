from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from src.responses import chatbot_response

app = Flask(__name__)
CORS(app)

# Serve the frontend
@app.route('/')
def home():
    return render_template('index.html')

# Chatbot API endpoint
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")
    user_id = data.get("user_id", "default")
    response = chatbot_response(user_message, user_id)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
