import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set")

client = OpenAI(api_key=api_key)

story = "I was little sad. and then I saw a flower. "

# Create a prompt that completes the story
prompt = f"""Complete the story delimited by triple backticks. 
 ```{story}```"""

# Get the generated response
def get_response(prompt):
    # Create a request to the chat completions endpoint
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content


response = get_response(prompt)
print(response)