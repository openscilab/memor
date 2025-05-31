# -*- coding: utf-8 -*-
"""Simple chat example
In this example, we demonstrate a simple chat application which uses history of the chat session.
In this example we use Mistral LLM to generate responses which is the same as OpenAI API LLM families."""
from pprint import pprint
from mistralai import Mistral

from memor import Prompt, Response, Session, Role, RenderFormat

MISTRAL_API_KEY = "YOUR_MISTRAL_API_KEY"  # Replace with your Mistral API key
MISTRAL_MODEL = "mistral-large-latest"
mistral_client = Mistral(api_key=MISTRAL_API_KEY)

session = Session(title="Simple Chat")
while True:
    try:
        user_input = input("You: ")
    except (EOFError, KeyboardInterrupt):
        break

    prompt = Prompt(
        message=user_input,
        role=Role.USER,
    )
    session.add_message(prompt)

    response_content = mistral_client.chat.complete(
        model=MISTRAL_MODEL,
        messages=session.render(RenderFormat.OPENAI)  # Render the whole session history
    ).choices[0].message.content
    response = Response(
        message=response_content,
        role=Role.ASSISTANT,
    )

    print(f"LLM: {response.message}")
    session.add_message(response)

# you can now access the session history
pprint(session.render(RenderFormat.OPENAI))
