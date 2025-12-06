from groq import Groq
import uuid
from datetime import datetime
import json
from typing import Dict

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
