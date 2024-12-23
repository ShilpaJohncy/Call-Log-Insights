from datetime import datetime

import anthropic
from flask import session

# Load the API key for Anthropic
with open('resources/anthropic-api-key.txt', 'r') as f:
    ANTHROPIC_API_KEY = f.read().strip()

anthropic_client = anthropic.Anthropic(
    api_key=ANTHROPIC_API_KEY,
)


# Utility function to format UTC date to human-readable format
def format_utc_date(date):
    try:
        return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d %B %Y %H:%M')
    except ValueError:
        return date


# Utility function to check if the current user has access to view the call
def has_access(call):
    for party in call['call_metadata']['parties']:
        if party['name'] == session["user_name"] and party['email'] == session["email"]:
            return True
    return False


# Utility function to ask a question to the Claude 3.5 Haiku model
def ask_anthropic(question, transcript):
    prompt = (
        f"The following is the transcript of a call:\n{transcript}\n\n"
        f"Based on the above transcript, can you answer the question:\n{question}\n\n"
    )

    # Query the Claude 3.5 Haiku model
    try:
        anthropic_response = anthropic_client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        )
        return anthropic_response.content[0].text, 200
    except Exception as e:
        return "Failed to process the request. \n {}".format(str(e)), 500
