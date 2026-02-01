import os
import sys
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key == None:
    raise RuntimeError("Hey! There is no API key")

client = genai.Client(api_key=api_key)




def main():

    

    parser = argparse.ArgumentParser(description="That is a Chatbot")
    parser.add_argument("user_prompt", type=str, help="Type some text after the run message. E.g. uv run main 'blabla'")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):
        antwort = client.models.generate_content(model='gemini-2.5-flash', contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt, temperature=0))

        candidates = antwort.candidates
        for candidate in candidates:
            messages.append(candidate)

        
        


        if antwort.usage_metadata == None:
            raise RuntimeError("Milord, we have not received any usage_metadata information!")
        
        if args.verbose == True:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {antwort.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {antwort.usage_metadata.candidates_token_count}")
            
        function_results = []
        if antwort.function_calls != None:
            for function_call in antwort.function_calls:
                # print(f"Calling function: {function_call}({function_call})")
                function_call_result = call_function(function_call, args.verbose)

                if function_call_result.parts == []:
                    raise Exception("Parts are empty")
                
                if function_call_result.parts[0].function_response == None:
                    raise Exception("function response is None")
                
                if function_call_result.parts[0].function_response.response == None:
                    raise Exception("function response.response is None")
                
                function_results.append(function_call_result.parts[0])

                if args.verbose == True:
                    print(f"-> {function_call_result.parts[0].function_response.response}")


        else:
            print("Response:")
            print(antwort.text)
            return
        
        messages.append(types.Content(role="user", parts=function_results))

    if antwort.function_calls == None:
        sys.exit("Error: maximum number exeeded and still no answer...")




# if __name__ == "__main__":
main()
