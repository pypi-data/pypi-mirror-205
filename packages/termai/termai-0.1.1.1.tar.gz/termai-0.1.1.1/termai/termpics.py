#!/usr/bin/env python3

import openai
import requests
import json
import base64
import os
from datetime import datetime

openai.api_key = os.environ["OPENAI_API_KEY"] # Set your API key as an environment variable

def generate_image(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}",
    }
    data = {
        "model": "image-alpha-001",
        "prompt": prompt,
        "num_images": 1,
        "size": "512x512",
        "response_format": "url",
    }
    response = requests.post("https://api.openai.com/v1/images/generations", headers=headers, data=json.dumps(data))
    response.raise_for_status()
    response_data = response.json()
    image_url = response_data["data"][0]["url"]
    return image_url

def save_image(image_url):
    response = requests.get(image_url)
    image_data = response.content
    image_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png"
    with open(image_name, "wb") as f:
        f.write(image_data)
    print(f"Image saved as {image_name}")

def main():
    prompt = input("Enter a prompt: ")
    image_url = generate_image(prompt)
    save_image(image_url)

if __name__ == "__main__":
    main()
