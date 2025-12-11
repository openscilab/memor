# -*- coding: utf-8 -*-
"""
Step 3: Mistral session picking up the same problem but giving a simpler session.
"""

from memor import Prompt, Session, Role, RenderFormat
from mistralai import Mistral
import pandas as pd
import re


SENSITIVE_REGEX = re.compile(
    r"(?:[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})|"   # email
    r"(?:\bX\d{8}\b)|"                                       # passport-like
    r"(?:\b(?:\d[ -]*?){13,16}\b)",                          # credit card
    flags=re.IGNORECASE
)
MAX_CHARS = 1500  # threshold for free LLM context window


df = pd.read_pickle('2_session_df.pkl')
print("Main session size:", len(df))
print(df.head())
df["contains_sensitive"] = df["message"].astype(str).str.contains(SENSITIVE_REGEX)

# Turn the status of ones with sensitive information or long to off:
df.loc[df["contains_sensitive"], "status"] = False
df.loc[df["message"].astype(str).str.len() > MAX_CHARS, "status"] = False

# Anonymize names inside remaining messages
NAME_REGEX = re.compile(r"\b[A-Z][a-z]{1,20}\s[A-Z][a-z]{1,20}\b")

def anonymize_names(text):
    return NAME_REGEX.sub("[REDACTED_NAME]", text)
df["message"] = df["message"].astype(str).apply(anonymize_names)


# Keep only active messages
df = df[df["status"] == True].reset_index(drop=True)
print("Main session size:", len(df))
print(df.head())

MISTRAL_API_KEY = "YOUR_MISTRAL_API_KEY"
MISTRAL_MODEL = "mistral-large-latest"
mistral_client = Mistral(api_key=MISTRAL_API_KEY)

session = Session(title="Trimmed Conversation")
session.from_dataframe(df)

p = Prompt(message="Can you summarize my plan?", role=Role.USER)
session.add_message(p)

mistral_response = mistral_client.chat.complete(
    model=MISTRAL_MODEL,
    messages=session.render(RenderFormat.OPENAI),
).choices[0].message.content

print(mistral_response)
