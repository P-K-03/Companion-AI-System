# AI Companion Chat System

## Project Structure

### 1. Data Setup
- **`chats/` folder**: Contains JSON files with conversation data between two friends (Tyler and Oliver)
  - `conversation_data.json`: Raw conversation data with messages from both users
  - `Tylers_chats.json`: Extracted messages from Tyler
  - `Olivers_chats.json`: Extracted messages from Oliver

### 2. Message Preprocessing (`messages_preprocessing.py`)

- Reads the raw conversation data from `conversation_data.json`
- Separates messages by sender (Tyler and Oliver)
- Creates individual JSON files for each person's chat history
- Prepares data for memory extraction and profile generation

### 3. Memory Extraction (`memory_extraction.py`)

- **Feature Extraction**: Analyzes each chat message to extract:
  - Communication style preferences
  - Emotional state indicators
  - Explicit facts mentioned
  - Implicit preferences
  - Timestamps
- **Pattern Aggregation**: Combines all extracted features to generate a comprehensive user profile including:
  - User preferences
  - Emotional patterns
  - Facts about the user
  - Behavioral insights
  - Any contradictions in communication
- **Generates two new JSON files**:
  - `processed/Tylers_memory_extracts.json`: Individual message-level insights
  - `processed/Tylers_profile.json`: Aggregated user profile with patterns and preferences

**Note**: A user Tyler's chats are processed and his profile is ready.

### 4. Personality Engine (`personality_engine.py`)

- **Load User Profile**: Reads the generated user profile from JSON to understand user characteristics
- **Memory Management**: 
  - Stores each conversation exchange in a ChromaDB vector database
  - Retrieves relevant past conversations based on semantic similarity to current input
  - Maintains conversation context across sessions
- **Personality Styles**: Supports multiple companion personalities from `personality_prompts` dictionary:
  - Each personality type has a unique system prompt
  - Personalities can be selected by the user for different interaction styles
  - Examples may include empathetic, analytical, humorous, supportive modes, etc.
- **Context-Aware Responses**: Combines user profile, relevant memories, and personality style to generate personalized responses

### 5. Main Chat Interface (`main.py`)

**How to use:**
- Initialize Groq API client and ChromaDB for conversation memory
- Select a personality type from the available options (displayed as numbered list)
- Start chatting with your AI companion
- Type your messages and receive contextually aware responses
- Exit by typing 'exit', 'quit', or 'bye'
- All conversations are automatically stored in vector database for future context retrieval

## Output
**Default personality**

<img width="1417" height="369" alt="Screenshot 2025-12-09 231312" src="https://github.com/user-attachments/assets/8c0e9f57-aff1-486f-a0d1-47e27a5f74c6" />

**Witty Friend Personality**

<img width="1412" height="699" alt="Screenshot 2025-12-09 231141" src="https://github.com/user-attachments/assets/5a1584cb-93bf-4b73-957f-2e4286d3ef3a" />


## Running the Project

### Prerequisites
- Python 3.8+
- `uv` package manager
- Groq API key

### Setup and Run

1. **Install dependencies using uv:**
   ```bash
   uv pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

3. **Run the companion chat:**
   ```bash
   uv run main.py
   ```

4. **Optional - Process new chat data:**
   ```bash
   # First, preprocess messages
   uv run messages_preprocessing.py
   
   # Then, extract memories and generate profile
   uv run memory_extraction.py
   ```

## Features

- Personality-based responses
- Semantic memory retrieval from past conversations
- User profile learning from chat history
- Multiple personality modes
- Persistent conversation storage
- Context-aware dialogue generation
