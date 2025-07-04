import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

generation_config = {
  "temperature": 1.0,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,

  system_instruction='''You are a Nutrition specialist and based on the food image provided by the user assume the following,
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
Don't mention its hard to calculate calories, just provide the appropriate value '''
)

def get_gemini_response(img,prompt):
   response = model.generate_content([img,prompt])
   return response.text

def get_file(uploaded_file):
  if uploaded_file:
    img=Image.open(uploaded_file)
    return img
  else:
     raise FileNotFoundError("No File uploaded!")

st.set_page_config("AI Nutrition App")
st.title("AI Nutrition App")

prompt=st.text_input('Enter the Prompt','Calculate the amount of calories')
uploaded_file = st.file_uploader("Choose a file")

btn=st.button('Submit')
if btn:
    img=get_file(uploaded_file)
    width, height = img.size
    st.image(img.resize((int(width*0.6), int(height*0.6))))
    st.write(get_gemini_response(img,prompt))
