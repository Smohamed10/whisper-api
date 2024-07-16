# app.py
from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

# Function to run whisper_like_script.py using subprocess
def run_whisper_script(audioFilePath, modelPath, language, translateToEnglish):
    command = f'python3 whisper_like_script.py {audioFilePath} {modelPath} {language} {translateToEnglish}'
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        transcription = result.stdout.decode('utf-8').strip()
        return transcription

    except subprocess.CalledProcessError as e:
        error_message = f'Error transcribing audio: {e.stderr.decode("utf-8").strip()}'
        return error_message

# Route to handle transcription requests
@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    data = request.get_json()

    # Extract parameters from JSON request
    audioFilePath = data.get('audioFilePath')
    modelPath = data.get('modelPath')
    language = data.get('language')
    translateToEnglish = data.get('translateToEnglish')

    # Perform transcription using WhisperManager
    from whisper_manager import WhisperManager
    manager = WhisperManager()
    manager.modelPath = modelPath
    manager.language = language
    manager.translateToEnglish = translateToEnglish

    try:
        # Assuming asynchronous handling for Flask with asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        transcription = loop.run_until_complete(manager.transcribe_audio(audioFilePath))
        return jsonify({'transcription': transcription})

    except Exception as e:
        return jsonify({'error': f'Error transcribing audio: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
