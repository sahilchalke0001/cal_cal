from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

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
    page_title="Cal_Cal",
    page_icon="🍕")

st.header("Health App")

# File uploader for image input
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Display the uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_container_width=True)

# Define input prompt for calorie estimation
input_prompt = """
You are an expert nutritionist tasked with analyzing the food items from the image
and calculating the total calories. Also, provide the details of each food item with its calorie intake in the following format:

1. Item 1 - number of calories
2. Item 2 - number of calories
---
---
"""

# Button to process the image
if st.button("Tell me the total calories"):
    if uploaded_file is None:
        st.error("Please upload an image.")
    else:
        try:
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(image_data, input_prompt)
            st.subheader("The Response is:")
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
else:
    st.info("Please upload an image and click 'Tell me the total calories'.")
