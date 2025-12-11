# Memor Examples
This folder contains examples demonstrating how to use the Memor library with various LLMs.

You should install the packages in the `requirements.txt` first by running `pip install -r requirements.txt`.
Following we provide a short description for each example.

## Simple Chat
A basic interactive chat loop using Memor to manage and render chat history.
Since single API calls don’t retain conversation history, you'd originally need to manually save your prior chat history in a array.
Memor simplifies this by providing `Session`, `Prompt`, and `Response` as an intuitive structure for multi-turn interactions.

## Dual-LLM Chat (Same Instruction)
An advanced interactive chat loop, simultaneously engaging with both Mistral and Google Gemini language models.
It leverages the Memor library to manage independent conversation histories for each LLM, ensuring contextual understanding.

## XML Usage
This example shows how XML can serve as a structured contract between a user, program logic, and an LLM using Memor.
By converting XML to a tree, modifying it programmatically, and having the LLM refine it, the workflow becomes both dynamic and model-friendly.

## Dataframe Usage
This example demonstrates how Memor can serialize an entire chat session into a dataframe, clean it using pandas, and rebuild a safe, compact version for use with another LLM.
A simulated multi-turn "premium" conversation is first exported as a DataFrame. In a second script, sensitive information (emails, IDs, passport-like strings) and oversized messages are automatically filtered out using regex rules and length constraints. The trimmed DataFrame is then converted back into a Memor Session and sent to another model like Mistral.
