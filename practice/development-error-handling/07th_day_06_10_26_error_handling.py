import os
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, APIError, RateLimitError
import json


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set. Check your .env file.")

client = OpenAI(api_key=api_key)

message = {
    "role": "user",
    "content": (
        "I have these notes with book titles and authors: "
        "New releases this week! The Beholders by Hester Musson, "
        "The Mystery Guest by Nita Prose. "
        "Please organize the titles and authors in JSON."
    )
}

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[message],
        response_format={"type": "json_object"}
    )

    print(response.choices[0].message.content)

except AuthenticationError:
    print("Please double check your authentication key and try again. The one provided is not valid.")

except RateLimitError:
    print("You hit the rate limit. Please wait and try again.")

except APIError as e:
    print(f"OpenAI API error: {e}")

except Exception as e:
    print(f"Unexpected error: {e}")

# Import the tenacity library
from tenacity import (retry, wait_random_exponential, stop_after_attempt)

# Add the appropriate parameters to the decorator
# Retry decorators with the parameters required to start retrying at an interval of 5 seconds, up to 40 seconds, and to stop after 4 attempts.
@retry(wait=wait_random_exponential(min=5, max=40), stop=stop_after_attempt(4))
def get_response(model, message):
    response = client.chat.completions.create(
        model=model,
        messages=[message]
    )
    return response.choices[0].message.content


print(get_response("gpt-4o-mini", {"role": "user", "content": "List ten holiday destinations."}))


# Function defining and calling

model = "gpt-4o-mini"

messages = [
    {
        "role": "user",
        "content": (
            "I bought the new smartphone last week. "
            "The camera quality is excellent and the battery lasts all day, "
            "but the screen scratches too easily. Overall, I like it."
        )
    }
]

function_definition = [
    {
        "type": "function",
        "function": {
            "name": "extract_review_info",
            "description": "Extract sentiment and key product features from a customer review.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sentiment": {
                        "type": "string",
                        "description": "The overall sentiment of the review, such as positive, negative, neutral, or mixed."
                    },
                    "features": {
                        "type": "array",
                        "description": "The product features mentioned in the review.",
                        "items": {
                            "type": "string"
                        }
                    }
                },
                "required": ["sentiment", "features"]
            }
        }
    }
]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    tools=function_definition,
    tool_choice={
        "type": "function",
        "function": {
            "name": "extract_review_info"
        }
    }
)

# Get the function arguments returned by the model
arguments = response.choices[0].message.tool_calls[0].function.arguments
# Convert JSON string to Python dictionary
review_info = json.loads(arguments)

print(review_info)