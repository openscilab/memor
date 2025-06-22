# -*- coding: utf-8 -*-
"""
Dual-LLM Chat Example with Mistral and Gemini.

This script creates a dual-LLM chat application, enabling simultaneous interaction with both Mistral and Google's Gemini models.
It leverages the Memor library to independently manage conversation history for each model and applies
a "chain of thought" system prompt to encourage structured reasoning from both AI models.
"""
from mistralai import Mistral
from google import genai
from google.genai import types
from memor import Prompt, Response, Session, Role, RenderFormat, LLMModel


MISTRAL_API_KEY = "YOUR_MISTRAL_API_KEY"
MISTRAL_MODEL = "mistral-large-latest"
mistral_client = Mistral(api_key=MISTRAL_API_KEY)


GOOGLE_AI_STUDIO_API_KEY = "YOUR_GOOGLE_AI_STUDIO_API_KEY"
GOOGLE_AI_STUDIO_MODEL = "gemini-2.0-flash"
gemini_client = genai.Client(api_key=GOOGLE_AI_STUDIO_API_KEY)


chain_of_thought_instruction = """
You are an AI assistant designed to engage in a 'chain of thought' reasoning process.
When responding, explicitly break down your thinking into steps.
First, state your initial understanding or immediate thoughts about the user's query.
Second, elaborate on any assumptions you are making or information you need.
Third, propose a step-by-step plan to address the query.
Fourth, execute your plan and provide the final answer or next step.
"""

system_prompt = Prompt(message=chain_of_thought_instruction, role=Role.SYSTEM)

session_mistral = Session(title="Mistral Chat")
session_gemini = Session(title="Gemini Chat")
session_mistral.add_message(system_prompt)

while True:
    try:
        user_input = input("You: ")
    except (EOFError, KeyboardInterrupt):
        break

    prompt = Prompt(
        message=user_input,
        role=Role.USER,
    )
    session_mistral.add_message(prompt)
    session_gemini.add_message(prompt)

    response_content_mistral = mistral_client.chat.complete(
        model=MISTRAL_MODEL,
        messages=session_mistral.render(RenderFormat.OPENAI)
    ).choices[0].message.content

    response_mistral = Response(
        message=response_content_mistral,
        role=Role.ASSISTANT,
    )

    response_content_gemini = gemini_client.models.generate_content(
        model=GOOGLE_AI_STUDIO_MODEL,
        # Google AI Studio models receive the system prompt as a separate parameter
        config=types.GenerateContentConfig(system_instruction=system_prompt.render(RenderFormat.STRING)),
        contents=session_gemini.render(RenderFormat.AI_STUDIO)
    )

    response_gemini = Response(
        message=response_content_gemini.text,
        role=Role.ASSISTANT,
        tokens=response_content_gemini.usage_metadata.total_token_count,
        model=LLMModel.GEMINI_2_FLASH,
    )

    print(f"LLM1 ({MISTRAL_MODEL}): {response_mistral.message}")
    print(f"LLM2 ({GOOGLE_AI_STUDIO_MODEL}): {response_gemini.message}")
    session_mistral.add_message(response_mistral)
    session_gemini.add_message(response_gemini)
