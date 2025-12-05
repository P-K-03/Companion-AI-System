import os
from groq import Groq
import chromadb
import json
from typing import Dict
from dotenv import load_dotenv

from prompts import personality_prompts

def get_chat_history():
    pass

def get_user_profile(profile_file_path: str) -> Dict:
    pass

def chat_with_companion(client: Groq, personality_type: str, user_profile: Dict, user_message: str):
    # chat_completion = client.chat.completions.create(
    #     messages=[
    #         {
    #             "role": "system",
    #             "content": personality_prompts[personality_type],
    #         },
    #         {
    #             "role": "user",
    #             "content": f"Use the preferences, emotional patterns, facts and behavioral insights of the user : {user_profile}",
    #         }, 
    #     ],
    #     model="openai/gpt-oss-20b",
    #     temperature=0.7,
    # )
    return "Response from Agent"

def main():
    load_dotenv()
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    profile_info: Dict = get_user_profile("processed/Tylers_profile.json")
    # user_message = ''
    personality_types = list(personality_prompts.keys())
    for i in range(0, len(personality_types)):
        print(f"{i+1}. {personality_types[i]}")
    
    flag = True
    while(flag):
        personality_type_input = input("Choose a personality from above: ")
        choice: int = int(personality_type_input)
        if choice < 1 and choice > len(personality_types):
            print("Invalid Personality Choice.")
        else:
            flag = False

    personality_type = personality_types[choice-1]
    while True:
        text = input("YOU: ")
        if text.lower() == 'bye':
            print("Bye Bye!")
            exit(0)
        print("COMPANION: ", end = "")
        print(chat_with_companion(client, personality_type, user_profile= profile_info, user_message = text))



if __name__ == '__main__':
    main()