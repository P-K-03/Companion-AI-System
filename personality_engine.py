import os
from groq import Groq
import chromadb
# from chromadb.config import Settings
import uuid
from datetime import datetime
import json
from typing import Dict
from dotenv import load_dotenv

from prompts import personality_prompts


def get_user_profile(profile_file_path: str) -> Dict:
    with open(profile_file_path, "r") as file:
        user_profile = json.load(file)
    return user_profile


def store_in_memory(user_msg:str, assistant_msg:str, conversation_id:str, memory_collection: str) -> None:
    memory_id = str(uuid.uuid4())
    combined_text = f"User: {user_msg}\nAssistant: {assistant_msg}"
    
    memory_collection.add(
        documents=[combined_text],
        ids=[memory_id],
        metadatas=[{
            "timestamp": datetime.now().isoformat(),
            "conversation_id": conversation_id,
            "user_msg": user_msg,
            "assistant_msg": assistant_msg
        }]
    )

def retrieve_relevant_memory(query:str, collection_name: str, top_k:int=2)-> str:
    results = collection_name.query(
        query_texts=[query],
        n_results=top_k
    )
    
    if results['documents'][0]:
        relevant_context = "\n\n".join([
            f"Past conversation:\n{doc}" 
            for doc in results['documents'][0]
        ])
        return relevant_context
    return ""


def chat_with_companion(client: Groq, personality_type: str, user_profile: Dict, user_input: str, conversation_history: str) -> str:
    conversation_id = str(uuid.uuid4())

    # retrieve relevant past memories
    relevant_memories = retrieve_relevant_memory(user_input, conversation_history, top_k=2)
    

    system_prompt_with_memory = f"""{personality_prompts[personality_type]}
    {user_profile}
    RELEVANT PAST CONVERSATIONS:
    {relevant_memories if relevant_memories else "No relevant past context."}
    Use this context naturally if relevant, but don't force it.
    """

    response = client.chat.completions.create(
        messages=[
        {"role": "system", "content": system_prompt_with_memory},
        {"role" : "user", "content" : user_input}
    ],
        model= "openai/gpt-oss-20b",
        temperature=0.7,
        max_tokens=300
    )
    
    assistant_reply = response.choices[0].message.content
    
    # store the conversation in vector database
    store_in_memory(user_input, assistant_reply, conversation_id, conversation_history)
    
    return assistant_reply

    # return "Response from Agent"

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



if __name__ == '__main__':
    main()