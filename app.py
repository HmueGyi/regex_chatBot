from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from src.responses import chatbot_response
import whisper
from pydub import AudioSegment
import tempfile
import os

app = Flask(__name__)
CORS(app)

# Load Whisper model once
model = whisper.load_model("small")

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

# Audio transcription endpoint
@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    audio_file = request.files['file']

    # Save uploaded audio to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
        audio_file.save(tmp.name)
        tmp_path = tmp.name

    wav_path = None
    try:
        # Convert to WAV
        audio = AudioSegment.from_file(tmp_path)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as wav_tmp:
            audio.export(wav_tmp.name, format="wav", parameters=["-ar", "16000"])

            wav_path = wav_tmp.name

        # Transcribe using Whisper (English only)
        result = model.transcribe(wav_path, language="en", fp16=False)
        transcript = result.get("text", "")

    except Exception as e:
        return jsonify({"error": f"Transcription failed: {str(e)}"}), 500

    finally:
        # Clean up temporary files
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        if wav_path and os.path.exists(wav_path):
            os.remove(wav_path)

    return jsonify({"transcript": transcript})

if __name__ == "__main__":
    app.run(debug=True)
