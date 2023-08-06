#!/usr/bin/env python
import openai
import sys
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def send_message(message):
    response = openai.Completion.create(model="text-davinci-003", prompt=message, max_tokens=200)
    return response.choices[0].text.strip()

def read_input():
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    elif len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return ""

input_data = read_input()

if input_data:
    user_input = f"Here's the output of a command: {input_data}. {sys.argv[1]}"
    response = send_message(user_input)
    print(response)
else:
    user_input = input("You: ")
    response = send_message(user_input)
    print(response)
