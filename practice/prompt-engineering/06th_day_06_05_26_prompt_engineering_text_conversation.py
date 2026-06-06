import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set")

client = OpenAI(api_key=api_key)
# Craft a prompt to change the email's tone
prompt = f""" Transform the sample email by changing its tone to be professional, positive, and user-centric.
```{sample_email}```"""

response = get_response(prompt)

print("Before transformation: \n", sample_email)
print("After transformation: \n", response)

# Craft a prompt to transform the text
prompt = f""" Transform the text delimited by triple backticks with the following two steps:
Step 1: Proofread it without changing its structure.
Step 2: Change the tone to be formal and friendly.
```{text}```"""

response = get_response(prompt)

print("Before transformation:\n", text)
print("After transformation:\n", response)

