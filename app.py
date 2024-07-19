import whisper
from flask import Flask, request, jsonify

app = Flask(__name__)

# Set up Whisper model
model = whisper.load_model("tiny")

# Function to handle temporary file cleanup (optional)
def cleanup_temp_file(temp_path):
  if temp_path and os.path.exists(temp_path):
    os.remove(temp_path)

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
    
    # Process the uploaded audio (Vercel specific)
    audio_bytes = file.read()
    
    # Transcribe the audio using Whisper
    result = model.transcribe(audio_bytes, language="ar", fp16=False, verbose=True)
    transcription = result['text']
    
    # Prepare response
    return jsonify({'transcription': transcription})
  
  except Exception as e:
    return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
  app.run(debug=True)
