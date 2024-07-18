import whisper
from flask import Flask, request, jsonify
from io import BytesIO
import numpy as np
import ffmpeg

app = Flask(__name__)

# Set up Whisper model
model = whisper.load_model("tiny")  # Use a smaller model if needed

def load_audio_from_bytesio(file_obj, sample_rate=16000):
    """
    Load audio from a BytesIO object and convert to a NumPy array.
    """
    out, _ = (
        ffmpeg.input('pipe:0', format='wav')
        .output('-', format='s16le', acodec='pcm_s16le', ac=1, ar=sample_rate)
        .run(input=file_obj.read(), capture_stdout=True, capture_stderr=True)
    )
    audio = np.frombuffer(out, np.int16).astype(np.float32) / 32768.0
    return audio

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
        
        # Read and process the file
        audio_data = BytesIO(file.read())
        audio_array = load_audio_from_bytesio(audio_data)
        
        # Transcribe the audio file using Whisper
        result = model.transcribe(audio_array, language="ar", fp16=False, verbose=True)
        transcription = result['text']
        
        # Return the transcription as JSON response
        return jsonify({'transcription': transcription})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
