A PoC in Python using Streamlit which takes a Video file and replace its audio with an AI Generated voice.
# Video Audio Replacement PoC

This project is a proof of concept (PoC) for replacing audio in video files using Google Cloud's Speech-to-Text and Text-to-Speech services and Azure OpenAI for transcription correction. The application is built using Streamlit for a simple web interface.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Project Structure](#project-structure)
  

## Features
- Upload video files (MP4, AVI, MOV).
- Extract audio from the video.
- Transcribe the audio using Google Cloud Speech-to-Text.
- Correct the transcription using Azure OpenAI.
- Generate new audio from the corrected transcription using Google Cloud Text-to-Speech.
- Replace the original audio in the video with the generated audio.

## Requirements
- Python 3.7 or higher
- Required Python packages:
  - streamlit
  - moviepy
  - google-cloud-speech
  - google-cloud-texttospeech
  - requests
  - python-dotenv

## Setup Instructions
1. **Clone the repository** (or download the files):
   ```bash
   git clone https://your-repo-url.git
   cd your-repo-directory
Install the required packages:

bash
Copy code
pip install -r requirements.txt
Set up Google Cloud:

Create a Google Cloud project and enable the Speech-to-Text and Text-to-Speech APIs.
Download your service account key in JSON format and save it in the project directory.
Set the path to your Google credentials in the code (replace path/to/your/google_credentials.json with your file name).
Set up Azure OpenAI:

Obtain your Azure OpenAI API key and endpoint URL.
Create a .env file in the project directory and add the following line:
makefile
Copy code
OPENAI_API_KEY=your_azure_openai_api_key
Usage
Run the Streamlit app:
bash
Copy code
streamlit run poc.py
Open the provided URL in your browser (usually http://localhost:8501).
Upload a video file using the file uploader.
Click the "Process Video" button to start processing.
The application will display the original and corrected transcriptions, and you can download the final video with the replaced audio.
Project Structure
bash
Copy code
.
├── poc.py                 # Main application script
├── requirements.txt       # Python package dependencies
├── .env                   # Environment variables (for Azure API key)
└── your_google_credentials.json # Google Cloud service account key
