const express = require('express');
const multer = require('multer');
const { exec } = require('child_process');
const path = require('path');

const app = express();
const port = process.env.PORT || 3000;
const upload = multer({ storage: multer.memoryStorage() });  // Use memory storage

const modelPath = path.resolve(__dirname, 'models', 'ggml-medium.bin');  // Ensure this path is correct

app.post('/transcribe', upload.single('audio'), (req, res) => {
    const audioBuffer = req.file.buffer;
    const audioFilePath = '/tmp/audio.wav';  // Temp path for storing audio file in memory

    // Write the audio buffer to a temporary file
    fs.writeFile(audioFilePath, audioBuffer, (err) => {
        if (err) {
            console.error(`Error writing audio file: ${err.message}`);
            return res.status(500).json({ error: 'Failed to write audio file' });
        }

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

            // Clean up the temporary file
            fs.unlink(audioFilePath, (err) => {
                if (err) {
                    console.error(`Error deleting temporary audio file: ${err.message}`);
                }
            });

            res.json({ transcription: stdout.trim() });
        });
    });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
