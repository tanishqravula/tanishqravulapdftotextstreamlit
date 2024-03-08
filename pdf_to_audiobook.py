import streamlit as st
import PyPDF2
from gtts import gTTS
import os
import base64

# Define the function for creating the download link
def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:audio/mp3;base64,{b64}" download="{file_label}.mp3">Download {file_label}</a>'
    return href

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
    st.markdown(get_binary_file_downloader_html(audio_file_path, "Audiobook"), unsafe_allow_html=True)

    # Display the audio player
    st.audio(audio_file_path, format="audio/mp3")

    # Clean up temporary audio file
    os.remove(audio_file_path)
