import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set")

client = OpenAI(api_key=api_key)


def get_response(prompt):
    # Create a request to the chat completions endpoint
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content


prompt = ("write a Python function that receives a list of 12 floats representing monthly sales data as input and, "
          "returns the month with the highest sales value as output.")

response = get_response(prompt)
print(response)

examples = """input = [10, 5, 8] -> output = 23
input = [5, 2, 4] -> output = 11
input = [2, 1, 3] -> output = 6
input = [8, 4, 6] -> output = 18
"""

# Craft a prompt that asks the model for the function
prompt = f"""You are provided with input-output examples delimited by triple backticks for a Python function where different factors are associated with project completion time. Each example includes numerical values for the factors and the corresponding estimated completion time. Write code for this function.
 ```{examples}```"""

response = get_response(prompt)
print(response)

function = """def calculate_area_rectangular_floor(width, length):
					return width*length"""

# Craft a multi-step prompt that asks the model to adjust the function
prompt = f"""Modify the function delimited by triple backticks as follows:
- Test if the inputs to the functions are positive, and if not, display appropriate error messages
- Return the area and perimeter of the rectangle.
```{function}```"""

response = get_response(prompt)
print(response)
