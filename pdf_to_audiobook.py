import streamlit as st
import PyPDF2
import base64
from gtts import gTTS
import os

st.title("PDF to Audiobook Converter")

# Upload PDF file
pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if pdf_file is not None:
    # Read the PDF and extract text
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(reader.pages)):
        text += reader.pages[page_num].extract_text()

    # Convert text to speech
    tts = gTTS(text)

    # Save the audio file
    audio_file_path = "output.mp3"
    tts.save(audio_file_path)

    # Provide download link for the audiobook
    with open(audio_file_path, "rb") as f:
        audio_bytes = f.read()
    audio_base64 = base64.b64encode(audio_bytes).decode()
    href = f'<a href="data:audio/mp3;base64,{audio_base64}" download="output.mp3">Download Audiobook</a>'
    st.markdown(href, unsafe_allow_html=True)

    # Display the audio player
    st.audio(audio_file_path, format="audio/mp3")

    # Clean up temporary audio file
    os.remove(audio_file_path)
