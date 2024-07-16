const express = require('express');
const multer = require('multer');
const path = require('path');
const WhisperManager = require('./WhisperManager');

const app = express();
const port = process.env.PORT || 3000;

const upload = multer({ storage: multer.memoryStorage() }); // Use memory storage

// Initialize Whisper-like model
const whisperManager = new WhisperManager('models/ggml-medium.bin', 'ar', false); // Adjust parameters as needed

// Root URL route
app.get('/', (req, res) => {
    res.send('Whisper API is running.');
});

async function initializeWhisper() {
    await whisperManager.init();
}

// Handle POST request to transcribe audio
app.post('/transcribe', upload.single('audio'), async (req, res) => {
    const audioFilePath = req.file.path;

    try {
        const transcription = await whisperManager.getTextFromAudio(audioFilePath);
        res.json({ transcription });
    } catch (error) {
        console.error('Error transcribing audio:', error);
        res.status(500).json({ error: 'Transcription failed' });
    }
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
    initializeWhisper().catch(error => {
        console.error('Failed to initialize Whisper-like model:', error);
        process.exit(1);
    });
});
