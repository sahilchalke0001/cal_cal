from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
#PIL (Python Imaging Library): Used to handle image files.

# Load all environment variables
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Pro Vision API and get response
def get_gemini_response(image_data, prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([image_data[0], prompt])
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Function to process uploaded image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data,
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(
    page_title="Cal Cal",
    page_icon="🍕")

st.header("🍕Health App🍕")

# Provide options for uploading or capturing an image
st.subheader("Input Options")
tab1, tab2 = st.tabs(["📤 Upload Image", "📸 Capture Photo"])

uploaded_file = None
captured_photo = None

# Tab for file uploader
with tab1:
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_container_width=True)

# Tab for capturing photo
with tab2:
    captured_photo = st.camera_input("Take a photo using your camera")
    if captured_photo:
        image = Image.open(captured_photo)
        st.image(image, caption="Captured Image.", use_container_width=True)

# Define input prompt for calorie estimation
input_prompt = """
You are an expert nutritionist tasked with analyzing the food items from the image
and calculating the total calories.Your name is Cal_Cal. Also, provide the details of each food item with its calorie intake in the following format:

Hey,My name is Cal_cal and there is the amount of calories.....

1. Item 1 - number of calories
2. Item 2 - number of calories
---
---
"""

if st.button("Tell me the total calories"):
    try:
            # Choose the appropriate image source
        if uploaded_file:
            image_data = input_image_setup(uploaded_file)
        elif captured_photo:
            image_data = input_image_setup(captured_photo)
        else:
            st.error("Please upload or capture an image.")
            st.stop()

        response = get_gemini_response(image_data, input_prompt)
        st.subheader("The Response is:")
        st.write(response)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
   

page_bg_img = '''
    <style>
        h2, h3 {
            text-align: center;
        }

    </style>
    '''
st.markdown(page_bg_img, unsafe_allow_html=True)