import whisper
from flask import Flask, request, jsonify
from io import BytesIO

app = Flask(__name__)

# Set up Whisper model
model = whisper.load_model("tiny")  # Use a smaller model

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
        
        # Read the file directly into memory
        audio_data = BytesIO(file.read())
        
        # Transcribe the audio file using Whisper
        result = model.transcribe(audio_data, language="ar", fp16=False, verbose=True)
        transcription = result['text']
        
        # Return the transcription as JSON response
        return jsonify({'transcription': transcription})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
