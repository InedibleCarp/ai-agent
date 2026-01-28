import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("missing API key.")

client = genai.Client(api_key=api_key)

def main():
    parser = argparse.ArgumentParser(description="Gemini Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
    
    generate_content(client, messages, args.verbose)
    
def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt),
    )
    
    if not response.usage_metadata:
        raise RuntimeError("failed API request.")
    
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
        
    if response.function_calls:
        function_results_list = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose)
            
            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
                or not function_call_result.parts[0].function_response.response
            ):
                raise RuntimeError(f"Empty function response for {function_call.name}")
                        
            if verbose:
                resp_dict = function_call_result.parts[0].function_response.response
                print(f"-> {resp_dict.get('result')}")
                
            function_results_list.append(function_call_result.parts[0])

    else:
        print(response.text)


if __name__ == "__main__":
    main()