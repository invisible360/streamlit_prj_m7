import streamlit as st
from PIL import Image 
from api_calling import note_generator, audio_transcriptor, quiz_generator
import markdown
from bs4 import BeautifulSoup

#title
st.title ("Note Summary and Quiz Generator", anchor=False)
st.markdown("Upload Maximum 3 images to get the summarize note and quiz")
st.divider()

#sidebar
with st.sidebar:
    images = st.file_uploader("Upload Image (Max 3)",
                              type=['jpg', 'jpeg', 'png'],
                              accept_multiple_files=True)

    if images:
        if len(images)>3:
            st.error ("More than 3 images are uploaded")
        else:
            st.markdown ("**Uploaded Images**")    
            cols = st.columns(len(images))
            for i, per_image in enumerate(images):
                with cols[i]:
                    st.image(per_image)

    difficulty_level = st.selectbox ("Select the difficulty level of quiz",
                                     ("Easy", "Medium", "Hard"),
                                     index=None)
    
    
    pressed = st.button ("Click the button to initiate AI", type="primary")

#removing all markdown-code from chatgpt
def remove_markdown(md_text):
    html = markdown.markdown(md_text)
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()


if pressed:
    if not images:
        st.error("Upload at least 1 image")
    if not difficulty_level:
        st.error("Select any of difficulty choice for the Quiz")
    #after providing successful image and level
    if images and difficulty_level:
        if len(images)>3:
            st.error ("Uploading more than 3 images are not allowed")
        else:
            # print(type(images))
            pil_images =[Image.open(image) for image in images]
            # print (type(pil_images))
            
            #note
            with st.container(border=True):
                st.subheader(":notebook: Your Notes")
                with st.spinner("Note is preparing..."):
                    generated_notes = note_generator(pil_images)
                    st.markdown(generated_notes)
            
            #audio
            with st.container(border=True):
                st.subheader(":microphone: Audio Transcription")
                mark_remove = remove_markdown(generated_notes)
                # st.text(mark_remove)
                with st.spinner("Preparing audio..."):
                    audio_transcript = audio_transcriptor(mark_remove)
                    st.audio(audio_transcript)
            
            #quiz
            with st.container(border=True):
                st.subheader(":notebook: Quiz and Answer")
                with st.spinner("Preparing quiz..."):
                    quizzes = quiz_generator(pil_images,difficulty_level)
                    st.markdown(quizzes)
    