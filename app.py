import os
import whisper
from flask import Flask, request, jsonify

app = Flask(__name__)

# Set up Whisper model
model = whisper.load_model("medium")

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the Whisper Transcription API!'}), 200
    
@app.route('/transcribe', methods=['POST'])
def transcribe():
    temp_path = None  # Initialize temp_path here
    try:
        # Ensure the file is part of the request
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        
        # Ensure a file is selected
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        # Save the file temporarily
        temp_path = os.path.join('temp', file.filename)
        file.save(temp_path)
        
        # Transcribe the audio file using Whisper
        result = model.transcribe(temp_path, language="ar", fp16=False, verbose=True)
        transcription = result['text']
        
        # Return the transcription as JSON response
        return jsonify({'transcription': transcription})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        # Clean up the temporary file if it was created
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == '__main__':
    os.makedirs('temp', exist_ok=True)  # Create the temp folder if it doesn't exist
    app.run(debug=True)