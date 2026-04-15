from google import genai
import streamlit as st
import os, io
from dotenv import load_dotenv
from gtts import gTTS


def connection_to_gemini (prompt):
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    #Initializing Client
    client = genai.Client(api_key=api_key)

    #response from gemini
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents= prompt
    )
    return response.text


#Note generator
def note_generator (images):
    prompt = """Summarize the picture in note format in language English at max 100 words
    make sure to add necessary markdown to differentiate the different section"""
    
    prompt_with_image = [images, prompt]
    notes = connection_to_gemini(prompt_with_image)
    return notes

def audio_transcriptor (text):
    speech = gTTS(text, lang="en", slow=False)
    audio_buffer = io.BytesIO() #creating temp memory in ram
    speech.write_to_fp(audio_buffer)
    return audio_buffer

def quiz_generator (images,difficulty):
     prompt = f"Generate 3 quizzes based on the {difficulty}. Make sure to add markdown to differentiate the options. Add correct answer too,after the quiz"

     prompt_with_level = [images, prompt]
     quize = connection_to_gemini(prompt_with_level)
     return quize


