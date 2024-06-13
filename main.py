import os
import time
import google.generativeai as genai
from dotenv import load_dotenv
import PIL.Image

load_dotenv()

api_key = os.environ["GEMINI_API_KEY"]

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

assets_folder = 'assets'
output_file = 'descriptions.txt'
image_files = [f for f in os.listdir(assets_folder) if os.path.isfile(os.path.join(assets_folder, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'))]

with open(output_file, 'w') as file:
    for idx, image_file in enumerate(image_files, start=1):
        img_path = os.path.join(assets_folder, image_file)
        img = PIL.Image.open(img_path)
        
        response = model.generate_content(["Write a one line generic description of the image.", img], stream=True)
        response.resolve()
        
        description = response.text.strip()
        file.write(f"{idx}. {image_file}: {description}\n")
        
        if idx % 15 == 0:
            time.sleep(60)

print(f"Descriptions have been written to {output_file}")
