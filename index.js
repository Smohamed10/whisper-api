const express = require('express');
const multer = require('multer');
const fs = require('fs');
const { exec } = require('child_process');
const path = require('path');

const app = express();
const port = process.env.PORT || 3000;
const upload = multer({ dest: 'uploads/' });

app.post('/transcribe', upload.single('audio'), (req, res) => {
    const audioFilePath = req.file.path;
    const modelPath = path.resolve(__dirname, 'models', 'ggml-medium.bin');

    // Run Whisper model inference
    const command = `path/to/whisper --model ${modelPath} --file ${audioFilePath}`;
    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return res.status(500).json({ error: 'Transcription failed' });
        }

        if (stderr) {
            console.error(`Stderr: ${stderr}`);
        }

        res.json({ transcription: stdout.trim() });
    });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
