import os
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, APIError, RateLimitError

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