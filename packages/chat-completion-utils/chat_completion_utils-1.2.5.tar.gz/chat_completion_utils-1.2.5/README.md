# ChatCompletion Utils

ChatCompletion Utils is a Python library that provides utility functions to very easily interact with OpenAI's Chat Completion API. It enables you to easily generate chat-friendly prompts, count tokens, and auto-select which model to use based on context length for the chat completion API endpoint. It also has a few other bells and whistles ;)

## Installation

Ensure you have installed the required packages:
```bash
poetry install
```

## Usage

First, set your OpenAI API key in the environment:

```bash
export OPENAI_API_KEY=<your_api_key>
```

Then, you can use the functions provided in the library:

```python
from chat_completion_utils import (
  llm, 
  _code_prompt, 
  num_tokens_from_messages, 
  select_model, 
  buid_prompt
)

# Generate a 'ChatCompletion' response with the OpenAI API

book_summary = llm(
  "Provide a brief summary of the following book series.",  # 'system' instruction
  "Harry Potter series.",                                   # 'user' prompt
  0.5                                                       # model temperature
)
print(book_summary)


# Use 'prompt partials' (e.g. `_code_prompt()`) to add pre-defined protective language to your prompts

web_app = llm(
  _code_prompt(),
  "geneate a React web application framework"
)


# Calculate tokens in a list of messages 
## - `llm()` bundles this functionality

messages = [
    {"role": "system", "content": "Translate the following English to French" },
    {"role": "user", "content": "Hello, how are you?" }
]
token_count = num_tokens_from_messages(messages, model="gpt-4")
print(token_count)


# Select the appropriate model to use based on token count
## - `llm()` bundles this functionality
## - auto switch to 'gpt-4-32k' if you need to, otherwise goes with the cheaper 'gpt-4' (or 'gpt-3.5-turbo' if you ask it to)

selected_model = select_model(messages)
print(selected_model)


# Construct prompt objects
## - `llm()` bundles this functionality
## - You shouldn't need to use this, but.. maybe I'm wrong. Go wild!

prompt = build_prompt(
  system_content=_code_prompt("Generate Ruby code for the given user prompt"),
  user_content="function to compute a factorial."
)
print(prompt)
```

## Functions
### `llm()`
Generate a chat-based completion using the OpenAI API.

#### Arguments
- system_instruction (str): The system instruction.
- user_input (str): The user input.
- temp (int): The temperature for controlling randomness of the output.

#### Returns
(str): The response from the model.

### `_code_prompt()`
Generate a code-only prompt.

#### Arguments
- prompt (str): The base prompt to modify.

#### Returns
(str): The modified prompt for code-only output.

### `num_tokens_from_messages()`
Count the number of tokens used by a list of messages.

#### Arguments
- messages (list): A list of messages.
- model (str): The model name.

#### Returns
(int): The number of tokens used by the list of messages.


### `select_model()`
Select the appropriate model based on token count.

#### Arguments
- messages (list): A list of messages.
- model_family (str): The model family (default: 'gpt-4').
- force (bool): Force the use of the specified model family if the token count is within limits.

#### Returns
(str): The selected model name.

### `buid_prompt()`
Build a list of messages to use as input for the OpenAI API.

#### Arguments
- system_content (str): The content for the system message.
- user_content (str): The content for the user message.
- messages (list): An optional list of existing messages.

#### Returns
(list): A list of messages to be used as input for the OpenAI API.

### Constants
The MODELS constant is a dictionary containing information about the supported models and their properties, such as the maximum number of tokens allowed.
