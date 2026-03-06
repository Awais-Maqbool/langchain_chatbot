# LangChain Chatbot

A modern AI-powered chat application built with Streamlit, LangChain, and Ollama. This chatbot provides intelligent conversations with context-aware responses using the Gemma 2B model.

## Features

- **Modern UI**: Professional dark-themed interface with Streamlit
- **Context-Aware**: Maintains conversation history for contextual responses
- **Multiple LLM Providers**: Support for Ollama (with OpenAI compatibility)
- **Session Management**: Track conversation turns with configurable limits
- **FastAPI Backend**: RESTful API for potential integrations

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **AI/ML**: LangChain, LangChain-Ollama
- **LLM**: Ollama (Gemma 2B)

## Prerequisites

- Python 3.11+
- Ollama installed and running locally

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd langchain_chatbot
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables:

```bash
cp .env.example .env
# Edit .env with your settings
```

5. Ensure Ollama is running:

```bash
ollama serve
ollama pull gemma:2b
```

## Usage

### Running the Chat Interface

```bash
streamlit run streamlit_app.py
```

The application will open at `http://localhost:8501`.

### Running the API Server

```bash
uvicorn src.main:app --reload
```

API documentation available at `http://localhost:8000/docs`.

## Project Structure

```
langchain_chatbot/
├── src/
│   ├── api/              # API endpoints
│   ├── config/           # Configuration settings
│   ├── core/             # Core utilities (logging, etc.)
│   ├── providers/        # LLM provider integrations
│   └── main.py           # FastAPI application
├── streamlit_app.py      # Streamlit chat interface
├── pyproject.toml        # Project metadata
└── requirements.txt      # Python dependencies
```

## Configuration

Configure your LLM provider in the settings:

- **Ollama**: Default provider using `gemma:2b` model
- **OpenAI**: Alternative provider (requires API key)

Edit `src/config/setting.py` to customize model parameters such as temperature, max tokens, and model selection.

## License

MIT License
