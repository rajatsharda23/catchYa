import os
import time
import google.generativeai as genai
from dotenv import load_dotenv
import PIL.Image
import streamlit as st

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("GEMINI_API_KEY is not set in the environment variables.")
    st.stop()

try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Failed to configure Generative AI model: {str(e)}")
    st.stop()

assets_folder = 'assets'
uploaded_files = st.file_uploader("Upload Image(s)", accept_multiple_files=True)

def process_images_and_display_descriptions(images):
    if not images:
        st.warning("Please upload one or more images.")
        return
    
    st.title("Image Descriptions")
    st.write("This model has a rate limit of 15 req per min, so after 15 images, it will wait for a min, and then continue :)")
    
    loading_text = st.empty()
    with st.spinner("Loading..."):
        descriptions = []

        for idx, uploaded_file in enumerate(images, start=1):
            try:
                img = PIL.Image.open(uploaded_file)
                response = genai.GenerativeModel('gemini-1.5-flash').generate_content(["Write a one line generic description of the image.", img], stream=True)
                response.resolve()
                description = response.text.strip()
            except Exception as e:
                description = f"Failed to generate description: {str(e)}"

            descriptions.append((uploaded_file.name, description))

            st.image(img, caption=f"{description}", use_column_width=True)
            st.markdown("---")

            if idx % 15 == 0:
                time.sleep(60)
            
            loading_text.text(f"Processing {idx}/{len(images)} images...")

    loading_text.empty()

if __name__ == "__main__":
    if uploaded_files:
        process_button = st.button("Process Images")
        if process_button:
            process_images_and_display_descriptions(uploaded_files)
    else:
        st.write("Upload one or more images using the file uploader above.")
