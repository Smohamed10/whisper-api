import os
import whisper
import tempfile
from flask import Flask, request, jsonify

app = Flask(__name__)

# Set up Whisper model
model = whisper.load_model("tiny")  # Use a smaller model if needed

@app.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        # Ensure the file is part of the request
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        
        # Ensure a file is selected
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        # Create a temporary file to store the uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_path = temp_file.name
            file.save(temp_path)
        
        # Transcribe the audio file using Whisper
        result = model.transcribe(temp_path, language="ar", fp16=False, verbose=True)
        transcription = result['text']
        
        # Delete the temporary file
        os.remove(temp_path)
        
        # Return the transcription as JSON response
        return jsonify({'transcription': transcription})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
