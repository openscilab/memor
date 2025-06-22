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
