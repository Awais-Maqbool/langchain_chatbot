# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LangChain Chatbot is an AI-powered chat application with two interfaces:
- **Streamlit UI** (`streamlit_app.py`) - Main chat interface with modern dark theme
- **FastAPI Backend** (`src/main.py`) - RESTful API for potential integrations

Uses LangChain with Ollama (Gemma 2B model) for AI-powered conversations.

## Commands

### Run the Chat Interface
```bash
streamlit run streamlit_app.py
```

### Run the API Server
```bash
uvicorn src.main:app --reload
```

API docs available at `http://localhost:8000/docs`

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Setup Ollama
```bash
ollama serve
ollama pull gemma:2b
```

## Code Flow & Architecture

### LangChain LCEL Chain Flow

```
User Input → ChatPromptTemplate → ChatOllama → StrOutputParser → Response
                ↑                                              ↓
            MessagesPlaceholder ← Chat History (context) ←───┘
```

### Streamlit Application Flow

```
streamlit_app.py
├── get_llm() → ChatOllama(model="gemma:2b", temperature=0)
├── get_chain() → ChatPromptTemplate | ChatOllama | StrOutputParser
├── Session State: chat_history[], max_turns=5
└── User Interaction:
    1. User types message → st.chat_input()
    2. HumanMessage added to chat_history
    3. chain.invoke({'question': prompt, 'chat_history': history[:-1]})
    4. Response (AIMessage) added to chat_history
    5. Display messages with st.chat_message()
```

### LangChain Components Used

| Component | Import | Purpose |
|-----------|--------|---------|
| ChatOllama | `langchain_ollama.ChatOllama` | LLM interface to Ollama |
| SystemMessage | `langchain_core.messages.SystemMessage` | System prompt |
| HumanMessage | `langchain_core.messages.HumanMessage` | User message |
| AIMessage | `langchain_core.messages.AIMessage` | AI response |
| ChatPromptTemplate | `langchain_core.prompts.ChatPromptTemplate` | Prompt builder |
| MessagesPlaceholder | `langchain_core.prompts.MessagesPlaceholder` | Chat history injection |
| StrOutputParser | `langchain_core.output_parsers.StrOutputParser` | Parse LLM output to string |

### Chain Composition (LCEL)

```python
# The | operator chains components together
chain = prompt | llm | StrOutputParser()
# Flow: prompt.format() → llm.invoke() → parser.parse()
```

### Message Flow in Chain

```
Input: {'question': 'Hello', 'chat_history': [HumanMessage(...), AIMessage(...)]}

1. ChatPromptTemplate formats:
   System: "You are a helpful assistant..."
   chat_history: [HumanMessage('Hi'), AIMessage('Hello!')]
   human: "Hello"

2. ChatOllama receives formatted messages, calls Ollama API

3. StrOutputParser extracts string from AIMessage

4. Returns: "Hello! How can I help you?"
```

## Project Structure

```
langchain_chatbot/
├── streamlit_app.py          # Main Streamlit UI (entry point)
├── src/
│   ├── main.py               # FastAPI app
│   ├── config/
│   │   └── setting.py       # Configuration
│   ├── core/
│   │   └── logging.py        # Logging utilities
│   ├── providers/
│   │   ├── ollama.py         # Ollama LLM provider
│   │   └── openai.py         # OpenAI LLM provider
│   └── api/
│       └── __init__.py       # API endpoints
├── pyproject.toml            # Project metadata
└── requirements.txt          # Dependencies
```

## Key Implementation Details

- **Model**: `gemma:2b` via Ollama (configurable in `get_llm()`)
- **Temperature**: 0 (deterministic responses)
- **Prompt**: System message + chat history + user question
- **Session Limits**: Max 5 conversation turns (configurable)
- **Caching**: `@st.cache_resource` for LLM and chain to avoid reinitialization
- **Error Handling**: Try-catch around chain invocation

## Customization Points

1. **Change Model**: Edit `model="gemma:2b"` in `get_llm()`
2. **Change Temperature**: Edit `temperature=0` in `get_llm()`
3. **Change System Prompt**: Edit the system message in `get_chain()`
4. **Add More Context**: Modify the prompt template in `get_chain()`
5. **Change Max Turns**: Edit `st.session_state.max_turns = 5`
