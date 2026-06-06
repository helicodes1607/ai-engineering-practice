import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set")

client = OpenAI(api_key=api_key)

def get_response(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content

# Define the purpose of the chatbot
chatbot_purpose = (
    "You are a customer support chatbot for an e-commerce company specializing in electronics. "
    "Your purpose is to help customers with product inquiries, order tracking, returns, refunds, "
    "warranty questions, and troubleshooting common issues with electronic gadgets. "
)

# Define audience guidelines
audience_guidelines = (
    "Your target audience is tech-savvy individuals who are interested in purchasing electronic gadgets "
    "such as headphones, smartphones, laptops, gaming accessories, smart home devices, and other electronics. "
)

# Define tone guidelines
tone_guidelines = (
    "Use a professional, helpful, and user-friendly tone. Provide clear step-by-step guidance when troubleshooting, "
    "ask relevant follow-up questions when needed, and keep responses concise, polite, and easy to understand. "
)


system_prompt = chatbot_purpose + audience_guidelines + tone_guidelines
response = get_response(system_prompt, "My new headphones aren't connecting to my device")
print(response)

# Behavioral control:
# Define the order number condition
order_number_condition = (
    "If the user asks about tracking, updating, canceling, returning, or checking the status of an order "
    "but does not provide an order number, ask the user to provide their order number before proceeding. "
)

# Define the technical issue condition
technical_issue_condition = (
    "If the user is reporting a technical issue, start your response with "
    "'I'm sorry to hear about your issue with ...' and replace the ellipsis with the specific product or issue mentioned by the user. "
)
# Create the base system prompt
base_system_prompt = chatbot_purpose + audience_guidelines + tone_guidelines
# Create the refined system prompt
refined_system_prompt = base_system_prompt + order_number_condition + technical_issue_condition

response_1 = get_response(refined_system_prompt, "My laptop screen is flickering. What should I do?")
response_2 = get_response(refined_system_prompt, "Can you help me track my recent order?")

print("Response 1: ", response_1)
print("Response 2: ", response_2)

