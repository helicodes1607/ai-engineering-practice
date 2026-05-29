import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

code = '''
def calculate_rectangle_area(length, width):
    area = length * width
    return area
'''

# Create a prompt that analyzes correctness of the code
prompt = f"""Determine the correctness of code delimited by triple backticks as follows:
Step 1: check the correct code syntax
Step 2: check whether function receives two inputs
Step 3: check whether function returns one output
Code: ```{code}```"""


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

#Chain of thought prompting: Requires LLMs to provide reasoning steps (thoughts) before giving answer
#Used for complex reasoning task
#Help reduce model errors

# Create the chain-of-thought prompt
prompt = """Q: Determine my friend's father's age in 10 years, given that he is currently twice my friend's age, and my friend is 20. Show step-by-step thinking.
A: Answer is"""

response = get_response(prompt)
print(response)

#One shot chain of thought prompt

# Define the example
example = """Q: Sum the even numbers in the following set: {9, 10, 13, 4, 2}.
             A: Even numbers: 10, 4, 2. Adding them: 10+4+2=16"""

# Define the question
question = """Q: Now this is a new set: {15, 13, 82, 7, 14}. Sum the even numbers.
              A:"""

# Create the final prompt
prompt = example + question
response = get_response(prompt)
print(response)

#Self consistency -> Generates multiple chain of thoughts by prompting the model several times.

# Create the self_consistency instruction
self_consistency_instruction = "Imagine three completely independent experts who reason differently are answering this question. The final answer is obtained by majority vote. The question is:"

# Create the problem to solve
problem_to_solve = "If you own a store that sells laptops and mobile phones. You start your day with 50 devices in the store, out of which 60% are mobile phones. Throughout the day, three clients visited the store, each of them bought one mobile phone, and one of them bought additionally a laptop. Also, you added to your collection 10 laptops and 5 mobile phones. How many laptops and mobile phones do you have by the end of the day?"

# Create the final prompt
prompt = self_consistency_instruction + problem_to_solve

response = get_response(prompt)
print(response)