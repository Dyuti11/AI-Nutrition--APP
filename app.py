import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import io

# Load API key from environment
load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Set model config
generation_config = {
  "temperature": 1.0,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

# Initialize model
model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  system_instruction='''
You are a Nutrition specialist and based on the food image provided by the user assume the following,
A standard recipe is used to prepare the food, i.e. traditional methods
It is a person's portion size
Answer the questions asked by the user.
If total calories were asked, remember to provide an approximate amount of calories list all the items along with the count, and also mention their respective calories. At last, provide the total calories.
The format is :
1. Item 1 (count) - no. of calories
2. Item 2 (Count) - no. of calories 
...
Total Calories:

If any other questions/suggestions were asked, answer them too.
Don't mention it's hard to calculate calories, just provide the appropriate value.
'''
)

# ⏳ Compress and convert image for Gemini input
def preprocess_image(uploaded_file):
    try:
        img = Image.open(uploaded_file)
        img.thumbnail((512, 512))  # Resize to save resources
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", optimize=True, quality=70)
        buffer.seek(0)
        return buffer
    except Exception as e:
        st.error("Failed to process image.")
        st.stop()

# 🤖 Send request to Gemini
def get_gemini_response(image_file, prompt):
    try:
        response = model.generate_content([image_file, prompt])
        return response.text
    except Exception as e:
        st.error("❌ Gemini API error: You may have hit a quota limit or sent a large input.")
        st.info("Try resizing the image or check your Google Cloud quota.")
        print("Gemini Error:", e)
        return None

# 🎨 Streamlit UI
st.set_page_config("AI Nutrition App")
st.title("🥗 AI Nutrition App")

prompt = st.text_input('Enter your prompt', 'Calculate the amount of calories')
uploaded_file = st.file_uploader("Upload a food image", type=["jpg", "jpeg", "png"])

if st.button('Submit'):
    if uploaded_file:
        processed_image = preprocess_image(uploaded_file)
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
        response = get_gemini_response(processed_image, prompt)
        if response:
            st.subheader("🍽 Nutrition Analysis:")
            st.write(response)
    else:
        st.warning("Please upload an image.")
