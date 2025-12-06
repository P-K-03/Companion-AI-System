import os
from groq import Groq
import chromadb
from typing import Dict
from dotenv import load_dotenv

from prompts import personality_prompts
from personality_engine import chat_with_companion, get_user_profile
def main():
    load_dotenv()

    # intialize clients
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    chroma_client = chromadb.Client()

    # get conversation history collection
    memory_collection = chroma_client.get_or_create_collection(
        name="conversation_memory",
        metadata={"hnsw:space": "cosine"}
    )
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
        if text.lower() in ['exit', 'quit', 'bye']:
            print("COMPANION: Take Care!")
            exit(0)
        print("COMPANION: ", end = "")
        
        print(chat_with_companion(client, personality_type, user_profile= profile_info, user_input = text, conversation_history= memory_collection))


if __name__ == "__main__":
    main()
