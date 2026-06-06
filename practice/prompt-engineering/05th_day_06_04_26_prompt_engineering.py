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

report = """
EcoSmart Bottle has shown strong market performance over the past year as more consumers look for sustainable and reusable alternatives to single-use plastic bottles. Customer feedback has been highly positive, with users praising the bottle's durable stainless-steel design, long-lasting temperature control, and leak-resistant lid. Sales increased after the company introduced new sizes, colors, and an optional built-in hydration reminder feature. The product has gained popularity among students, office workers, travelers, and fitness enthusiasts. Overall, EcoSmart Bottle is positioned as a practical, eco-friendly product that supports healthier hydration habits while reducing plastic waste.
"""

product_description = """
EcoSmart Bottle is a reusable stainless-steel water bottle designed to keep drinks hot or cold for long periods while helping reduce single-use plastic waste. It features double-wall insulation, a leak-resistant lid, a durable lightweight body, and an optional hydration reminder feature. The bottle is suitable for daily use at school, work, the gym, or while traveling. EcoSmart Bottle offers a convenient and sustainable hydration solution for people who want a reliable, stylish, and environmentally friendly alternative to disposable bottles.
"""
# Craft a prompt to summarize the report
prompt = f""" Summarize the report delimited  by triple backticks in maximum five sentences: 
```{report}```"""

response = get_response(prompt)

print("Summarized report: \n", response)

# Craft a prompt to expand the product's description
prompt = f""" Expand the product description delimited  by triple backticks and write a one paragraph comprehensive overview capturing the key information of the product: unique features, benefits, and potential applications.: 
```{product_description}```"""

response = get_response(prompt)

print("Original description: \n", product_description)
print("Expanded description: \n", response)

