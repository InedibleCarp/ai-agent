import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("missing API key.")

client = genai.Client(api_key=api_key)

def main():
    parser = argparse.ArgumentParser(description="Gemini Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
        
    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=messages
    )
    
    if not response.usage_metadata:
        raise RuntimeError("failed API request.")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    print(response.text)


if __name__ == "__main__":
    main()
