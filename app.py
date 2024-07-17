import os
import whisper
from flask import Flask, request, jsonify
from tqdm import tqdm

app = Flask(__name__)

# Set up Whisper model and output folder
model = whisper.load_model("base")
output_folder = "transcriptions"  # Adjust this path as per your setup

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
        
        # Save the file temporarily
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(temp_path)
        
        # Transcribe the audio file using Whisper
        result = model.transcribe(temp_path, language="ar", fp16=False, verbose=True)
        transcription = result['text']
        
        # Prepare filename for saving transcription
        filename_no_ext = os.path.splitext(file.filename)[0]
        output_filepath = os.path.join(output_folder, filename_no_ext + '.txt')
        
        # Ensure the output directory exists
        os.makedirs(output_folder, exist_ok=True)
        
        # Save transcription to a text file
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(transcription)
        
        # Return the transcription as JSON response
        return jsonify({'transcription': transcription})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'temp'  # Define your upload folder
    app.run(debug=True)
