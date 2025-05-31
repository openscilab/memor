# -*- coding: utf-8 -*-
"""Multi LLM chat example

In this example, we're using one of the most controversial questions in human history: "Do the ends ever justify the means?"
This question sits at the heart of countless ethical, political, philosophical debates, and modern policymaking.
To explore the contrast in worldviews, we present two opposing perspectives (taken role by two LLMs).
1. The first is an ethical idealist, who argues that the process matters just as much as — if not more than — the outcome, and that compromising principles undermines the integrity of any goal. We give this role to Mistral.
2. The second is from a Machiavellian strategist, who believes that achieving a desirable outcome can legitimize morally ambiguous actions, prioritizing results over the path taken. We give this role to Google AI Studio.
These dialogues illustrate the deep philosophical divide between consequentialism and deontological ethics. Therefore that makes a great example for a multi agent chat application using two different LLMs: Mistral and Google AI Studio.
"""
from mistralai import Mistral
from google import genai

from memor import PromptTemplate
from memor import Prompt, Response
from memor import Session
from memor import Role, RenderFormat, LLMModel

session = Session(title="Ethical Debate") # Create a new session for the chat
prompt = Prompt(
    message="Do the ends ever justify the means?",
    role=Role.USER,
)

MISTRAL_API_KEY = "YOUR_MISTRAL_API_KEY"
MISTRAL_MODEL = "mistral-large-latest"
mistral_client = Mistral(api_key=MISTRAL_API_KEY)

ethical_idealist_template = PromptTemplate(
    content="{instruction}\n\n{prompt[message]}",
    custom_map={
        "instruction": "You are an ethical idealist who believes that how we act matters just as much — if not more — than what we achieve."
            "You value principles like honesty, justice, and human dignity, even when they complicate the path to success."})

prompt.update_template(ethical_idealist_template)
chat_response = mistral_client.chat.complete(
    model = MISTRAL_MODEL,
    messages = [ #TODO: need change and use prompt.render(RenderFormat.OPENAI)
        {
            "role": Role.SYSTEM.value,
            "content": ethical_idealist_template.custom_map["instruction"]
        },
        {
            "role": Role.USER.value,
            "content": prompt.message
        }
    ]
)
for choice in chat_response.choices:
    print(f"Mistral response: {choice.message.content}")
    response = Response(
        message=choice.message.content,
        role=Role.ASSISTANT,
        tokens=chat_response.usage.total_tokens,
        model=chat_response.model,
    )
    prompt.add_response(response)
session.add_message(prompt)


# Setting up Google AI Studio client
GOOGLE_AI_STUDIO_API_KEY = "YOUR_GOOGLE_AI_STUDIO_API_KEY"
GOOGLE_AI_STUDIO_MODEL = "gemini-2.0-flash"
gemini_client = genai.Client(api_key=GOOGLE_AI_STUDIO_API_KEY)

machiavellian_strategist_template = PromptTemplate(
    content="{instruction}\n\n{prompt[message]}",
    custom_map={
        "instruction": "You are a pragmatic strategist inspired by Niccolò Machiavelli."
            "You believe power, stability, and success often require morally ambiguous choices."
            "You prioritize results over intentions and see ethical rules as tools, not absolutes."})

prompt.update_template(machiavellian_strategist_template)

chat_content = gemini_client.models.generate_content(
    model=GOOGLE_AI_STUDIO_MODEL,
    contents=prompt.render(RenderFormat.AI_STUDIO)
)

response = Response(
    message=chat_content.text,
    role=Role.ASSISTANT,
    tokens=chat_response.usage.total_tokens,
    model=LLMModel.GEMINI_2_FLASH,
)
prompt.add_response(response)
session.add_message(prompt)

session.save(f"{session.title.lower().replace(' ', '-')}.json")  # Save the session with all messages
print(session)
