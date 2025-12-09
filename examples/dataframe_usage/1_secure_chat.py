# -*- coding: utf-8 -*-
"""
Step 1: ...
"""

from memor import Prompt, Response, Session, Role, RenderFormat
from mistralai import Mistral


sample_messages = [
    "Hey, I need help planning my 3-month Europe trip. I'll be visiting France, Italy, and Germany.",
    "My budget is around $7,200. I'm trying to keep track of flight costs, hotels, and food.",
    "Also here is my email just in case: personal.email@example.com",
    "I'm thinking of booking a multi-city flight. Found one for $1240 on Lufthansa.",
    "Here's a chunk of my notes: " + "lorem ipsum " * 400,  # intentionally long
    "My passport number is X12345678. Please remind me to renew it.",
    "Can you help me create a daily itinerary for France first?",
]

system_instruction = "You are a helpful assistant. Provide concise and accurate answers."
system_prompt = Prompt(message=system_instruction, role=Role.SYSTEM)

MISTRAL_API_KEY = "YOUR_MISTRAL_API_KEY"
MISTRAL_MODEL = "mistral-large-latest"
mistral_client = Mistral(api_key=MISTRAL_API_KEY)

session = Session(title="Private Chat")
session.add_message(system_prompt)

for msg in sample_messages:
    p = Prompt(message=msg, role=Role.USER)
    session.add_message(p)

    response = mistral_client.chat.complete(
        model=MISTRAL_MODEL,
        messages=session.render(RenderFormat.OPENAI)
    ).choices[0].message.content

    r = Response(
        message=response,
        role=Role.ASSISTANT,
    )
    session.add_message(r)

df = session.to_dataframe()
df.to_csv('2_session_df.csv')
