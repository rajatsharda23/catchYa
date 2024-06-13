import os
import google.generativeai as genai
from dotenv import load_dotenv
import PIL.Image
load_dotenv()

api_key = os.environ["GEMINI_API_KEY"]

genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-1.5-flash')

img = PIL.Image.open('assets/img7.png')

response = model.generate_content(["Write a one line generic description of the image.", img], stream=True)
response.resolve()
print(response.text)