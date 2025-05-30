# -*- coding: utf-8 -*-
"""Simple chat example"""
import os
from dotenv import load_dotenv

from mistralai import Mistral
from google import genai

from memor import PromptTemplate
from memor import Prompt, Response
from memor import Session
from memor import Role

load_dotenv()
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY", "YOUR_API_KEY")
if not MISTRAL_API_KEY:
    raise ValueError("Please set the MISTRAL_API_KEY environment variable.")
MISTRAL_MODEL = os.environ.get("MISTRAL_MODEL", "mistral-large-latest")

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "YOUR_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Please set the GOOGLE_API_KEY environment variable.")
GOOGLE_MODEL = os.environ.get("GOOGLE_MODEL", "gemini-2.0-flash")


client = Mistral(api_key=MISTRAL_API_KEY)
chat_response = client.chat.complete(
    model = MISTRAL_MODEL,
    messages = [
        {
            "role": "user",
            "content": "What is the best French cheese?",
        },
    ]
)
print(chat_response.choices[0].message.content)


client = genai.Client(api_key=GOOGLE_API_KEY)
response = client.models.generate_content(
    model=GOOGLE_MODEL,
    contents="Explain how AI works in a few words"
)
print(response.text)
