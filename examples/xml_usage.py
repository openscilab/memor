"""
Structured Planning Example Using XML with Memor.

This demo shows how XML can serve as a lightweight, LLM-friendly structured format.
We store a user's plan as XML, parse it into a tree, modify it programmatically,
then send the updated structure to the LLM for refinement.
"""

from pprint import pprint
from mistralai import Mistral
from memor import Prompt, Response, Session, Role, RenderFormat

MISTRAL_API_KEY = "YOUR_KEY"
MODEL = "mistral-large-latest"
client = Mistral(api_key=MISTRAL_API_KEY)

initial_xml = """
<plan>
    <goal>Prepare for machine learning exam</goal>
    <steps>
        <step>Review lecture slides</step>
        <step>Re-read key textbook chapters</step>
    </steps>
</plan>
"""

session = Session(title="XML Planner Session")

prompt = Prompt(message=initial_xml, role=Role.USER)
session.add_message(prompt)

print("Initial parsed plan:")
pprint(prompt.xml_tree)

tree = prompt.xml_tree
tree["plan"][0]["steps"].append({"step": [{"text": "Solve past exam questions"}]})

prompt.update_message_from_xml(tree)

print("Updated XML plan:")
print(prompt.message)

system_instruction = """
You are a study assistant.
Given an XML <plan>, improve the steps by making them more specific or actionable.
Return ONLY an updated <plan> XML, same structure.
"""

system_prompt = Prompt(message=system_instruction, role=Role.SYSTEM)
session.add_message(system_prompt)
session.add_message(prompt)

response_text = client.chat.complete(
    model=MODEL,
    messages=session.render(RenderFormat.OPENAI)
).choices[0].message.content

response = Response(message=response_text, role=Role.ASSISTANT)
session.add_message(response)

print("LLM-refined XML:")
print(response.message)

print("Refined plan (as structured data):")
pprint(response.xml_tree)
