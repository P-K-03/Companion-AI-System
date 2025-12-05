import os
import json
from groq import Groq
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime
import chromadb

from prompts import (
    extract_message_features_prompt,
    memory_extractor_system_prompt,
    extract_aggregate_pattern_prompt,
)


# Model to get structured output
class ExtractFeaturesSchema(BaseModel):
    communication_syle_preference: List[str]
    emotional_state_indicators: List[str]
    explicit_facts: List[str]
    implicit_preferences: List[str]
    timestamp: datetime


class AggregatePatternSchema(BaseModel):
    preferences: List[str]
    emotional_patterns: List[str]
    facts: List[str]
    behavioural_insights: List[str]
    contradictions: List[str]
    generated_at: datetime = datetime.now()


def extract_features_from_chat(
    client: Groq, source_chats_path: str, dest_chats_path: str
):
    with open(source_chats_path, "r") as file:
        Tylers_chats = json.load(file)
    # print(json.dumps(Tylers_chats, indent=4))

    # Get all the chats
    messages = []
    for element in Tylers_chats:
        messages.append(element["text"])

    # Extract insights
    extracts = []
    for i in range(0, len(messages)):
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": memory_extractor_system_prompt,
                },
                {
                    "role": "user",
                    "content": f"{extract_message_features_prompt} {messages[i]}",
                },
            ],
            model="openai/gpt-oss-20b",
            temperature=0.7,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "extract_output",
                    "schema": ExtractFeaturesSchema.model_json_schema(),
                },
            },
        )
        # print(chat_completion.choices[0].message.content)
        extracts.append(chat_completion.choices[0].message.content)
        print(f"Message {i+1} processed")
    print(f"Length of extracts list is : {len(extracts)}")

    # Save the features to a json file
    with open(dest_chats_path, "w", encoding="utf-8") as file:
        file.write("[")
        for i in range(0, len(extracts)):
            # json.dump(entry, file)
            file.write(str(extracts[i]))

            if i != len(extracts) - 1:
                file.write(",")
        file.write("]")
    print("Data extracted from all text messages")
    return extracts


def aggregate_patterns_from_features(
    client: Groq,
    extracted_features_path: str,
    save_to: str,
    extracts: List[Dict] = None,
):

    print("Loading insights")
    if extracts is None:
        with open(extracted_features_path, "r") as file:
            data = json.load(file)
        extracts = data

    print("Generating user profile")
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": memory_extractor_system_prompt,
            },
            {
                "role": "user",
                "content": f"{extract_aggregate_pattern_prompt} {extracts}",
            },
        ],
        model="openai/gpt-oss-20b",
        temperature=0.7,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "extract_output",
                "schema": AggregatePatternSchema.model_json_schema(),
            },
        },
    )
    # print(chat_completion.choices[0].message.content)

    print("Generated User Profile")
    # Save the PROFILE to a json file
    with open(save_to, "w", encoding="utf-8") as file:
        # json.dump(entry, file)
        file.write(str(chat_completion.choices[0].message.content))
    print(f"Saving the profile data in {save_to}")


def save_chats(path_to_db: str, conversation_file_path: str, collection_name: str):
    chroma_client = chromadb.PersistentClient(path=path_to_db)
    collection = chroma_client.get_or_create_collection(name=collection_name)
    with open(conversation_file_path, "r") as file:
        chats = json.load(file)

    ids = ["id" + str(i) for i in range(0, len(chats))]
    documents = [chat["text"] for chat in chats]
    metadatas = []
    for chat in chats:
        element = {}
        element["sender"] = chat["sender_id"]
        element["timestamp"] = chat["timestamp"]
        metadatas.append(element)

    collection.add(ids=ids, documents=documents, metadatas=metadatas)
    print(
        f"Saved user chats in vector database at: ./{path_to_db} in collection: {collection_name}"
    )


def main():
    # Load the environment variables
    load_dotenv()

    # Initialize the Groq client
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    # Extracting information from the chats
    extract_features_from_chat(
        client = client, source_chats_path = "chats/Tylers_chats.json", dest_chats_path = "processed/Tylers_memory_extracts.json"
    )

    # Create user profile
    aggregate_patterns_from_features(
        client = client, extracted_features_path = "processed/Tylers_memory_extracts.json", save_to = "processed/Tylers_profile.json"
    )

    # Save the chats to a vector database
    save_chats(path_to_db = "chromaDB", conversation_file_path = "chats/Tylers_chats.json", collection_name = "Tyler")


if __name__ == "__main__":
    # This block executes only when the script is run directly.
    main()
