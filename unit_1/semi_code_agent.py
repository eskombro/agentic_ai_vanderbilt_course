from litellm import completion
from typing import List, Dict

import os
api_key = os.getenv('OPENAI_API_KEY')

def generate_response(messages: List[Dict]) -> str:
    """Call LLM to get response"""
    response = completion(
        model="openai/gpt-5-mini",
        messages=messages,
        max_tokens=1024
    )
    return response.choices[0].message.content

def extract_code_block(response: str) -> str:
    """Extract code block from response"""
    if not '```' in response:
        return response

    code_block = response.split('```')[1].strip()
    if code_block.startswith("python"):
        code_block = code_block[6:]

    return code_block

initial_prompt = """
    You are a software engineer that is expert in python and help users create python clean code functions to solve their problems.
    Start by asking a user which function they want to create. Immediately create the function and present it to the user in a ```python code block```.
"""

user_prompts = [input("What do you need help with?"), "please document the function", "please add test cases using unittest framework"]

messages = [
    {"role": "system", "content": initial_prompt},
    {"role": "user", "content": user_prompts[0]}
]

for user_prompt in user_prompts:
    print(f"--------------------------------\nUSER PROMPT:")
    print(user_prompt)
    response = generate_response(messages)
    print(f"--------------------------------\nRESPONSE:")
    print(response)
    messages.append({"role": "assistant", "content": extract_code_block(response)})
    messages.append({"role": "user", "content": user_prompt})