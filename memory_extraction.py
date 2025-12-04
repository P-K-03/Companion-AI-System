import os
import json
from groq import Groq
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Dict

from prompts import extract_message_features_prompt, memory_extractor_system_prompt, extract_aggregate_pattern_prompt


# Model to get structured output
class ExtractFeaturesSchema(BaseModel):
    communication_syle_preference: List[str]
    emotional_state_indicators: List[str]
    explicit_facts: List[str]
    implicit_preferences: List[str]

class AggregatePatternSchema(BaseModel):
    preferences: List[str]
    emotional_patterns: List[str]
    facts: List[str]  
    behavioural_insights: List[str]
    contradictions: List[str]

def extract_features_from_chat(client: Groq, source_chats_path: str, dest_chats_path: str):
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
        file.write('[')
        for i in range(0, len(extracts)):
            # json.dump(entry, file)
            file.write(str(extracts[i]))

            if i != len(extracts)-1:
                file.write(',')
        file.write(']')
    print("Data extracted from all text messages")
    return extracts

def aggregate_patterns_from_features(client: Groq, extracted_features_path: str, save_to: str, extracts: List[Dict] = None):
    if extracts is None:
        with open(extracted_features_path, "r") as file:
            data = json.load(file)
        extracts = data
    
    # aggregate_patterns = []
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

    # Save the PROFILE to a json file
    with open(save_to, "w", encoding="utf-8") as file:
        # json.dump(entry, file)
        file.write(str(chat_completion.choices[0].message.content))
    print("Generated User Profile")
        


def main():
    # Load the environment variables
    load_dotenv()

    # Initialize the Groq client
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    # Extracting information from the chats
    # extract_features_from_chat(
    #     client, "chats/Tylers_chats.json", "processed/Tylers_memory_extracts.json"
    # )

    # Create user profile
    aggregate_patterns_from_features(client,'processed/Tylers_memory_extracts.json', 'processed/Tylers_profile.json')

main()