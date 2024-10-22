import streamlit as st
import os
from moviepy.editor import VideoFileClip, AudioFileClip
from google.cloud import speech
from google.cloud import texttospeech
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# Set up Google Cloud and Azure OpenAI credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "dark-diagram-439418-p0-a97b493c7bef.json"
AZURE_OPENAI_KEY = os.getenv("OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = "https://internshala.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview"

def transcribe_audio(audio_file):
    client = speech.SpeechClient()
    
    with open(audio_file, "rb") as audio_file:
        content = audio_file.read()
    
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    
    response = client.recognize(config=config, audio=audio)
    return " ".join([result.alternatives[0].transcript for result in response.results])

def correct_transcription(text):
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_KEY
    }
    
    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that corrects grammatical mistakes and removes filler words."},
            {"role": "user", "content": f"Please correct the following text, removing any grammatical mistakes and filler words like 'um' and 'uh': {text}"}
        ]
    }
    
    response = requests.post(AZURE_OPENAI_ENDPOINT, headers=headers, json=payload)
    response_data = json.loads(response.text)
    
    return response_data['choices'][0]['message']['content']

def text_to_speech(text):
    client = texttospeech.TextToSpeechClient()
    
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Journey-D",
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
    
    return "output.mp3"

def replace_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    final_clip = video.set_audio(audio)
    output_path = "output_video.mp4"
    final_clip.write_videofile(output_path)
    return output_path

st.title("Video Audio Replacement PoC")

uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    st.video(uploaded_file)
    
    if st.button("Process Video"):
        with st.spinner("Processing..."):
            # Save the uploaded file
            video_path = "temp_video.mp4"
            with open(video_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Extract audio from video
            video = VideoFileClip(video_path)
            audio_path = "temp_audio.wav"
            video.audio.write_audiofile(audio_path)
            
            # Transcribe audio
            transcription = transcribe_audio(audio_path)
            st.text("Original Transcription:")
            st.write(transcription)
            
            # Correct transcription
            corrected_text = correct_transcription(transcription)
            st.text("Corrected Transcription:")
            st.write(corrected_text)
            
            # Generate new audio
            new_audio_path = text_to_speech(corrected_text)
            
            # Replace audio in video
            output_video_path = replace_audio(video_path, new_audio_path)
            
            st.success("Video processing complete!")
            st.video(output_video_path)
            
            # Clean up temporary files
            os.remove(video_path)
            os.remove(audio_path)
            os.remove(new_audio_path)
            os.remove(output_video_path)

st.text("Note: This PoC requires proper setup of Google Cloud and Azure OpenAI credentials.")