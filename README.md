# Life Insurance Support Assistant

AI-powered chatbot that helps users with life insurance inquiries using LangGraph, OpenAI, and FAISS for intelligent RAG-based conversations.

## Features

- **LangGraph Workflow**: Complex agent orchestration with retrieval and generation nodes
- **RAG Architecture**: FAISS vector store with semantic search for accurate responses
- **Conversational Context**: Maintains chat history across turns
- **Dual Interface**: CLI for interactive chat and FastAPI REST API
- **Configurable Knowledge Base**: Easily extensible life insurance domain knowledge
- **Session Management**: Multi-user conversation tracking

## Quick Start

### 1. Installation (windows 11pro)

```bash
# create virtual env
python -m venv venv

# activate virtual env
venv\scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
```

### 3. Run CLI

```bash
python -m app.cli.chat_cli
```

### 4. Run API Server

```bash
 uvicorn main:app 
 or
 python main.py
```

API will be available at `http://localhost:8000`

## Usage

### CLI Interface

Interactive chat with commands:
- Type your question naturally
- `clear` - Reset conversation
- `quit` / `exit` - Exit application

### API Endpoints

**Chat**
```bash
POST /chat
{
  "message": "What is term life insurance?",
  "session_id": "user123"
}
```

**Get History**
```bash
GET /sessions/{session_id}/history
```

**Clear Session**
```bash
DELETE /sessions/{session_id}
```

**List Sessions**
```bash
GET /sessions
```

## Architecture

```
User Query
    ↓
LangGraph Agent
    ↓
├── Retrieve Context (FAISS Vector Store)
    ↓
└── Generate Response (OpenAI GPT-4)
    ↓
Response + Updated Context
```

### Components

- **`app/agent/insurance_agent.py`**: LangGraph workflow with RAG pipeline
- **`app/vector_store/faiss_store.py`**: FAISS vector store management
- **`app/knowledge_base/insurance_data.py`**: Life insurance domain knowledge
- **`app/api/server.py`**: FastAPI REST endpoints
- **`app/cli/chat_cli.py`**: Interactive CLI interface

### LangGraph Workflow

1. **Retrieve Context**: Queries FAISS with user input, returns top-k relevant documents
2. **Generate Response**: Combines context + conversation history + user query → LLM generates answer

## Knowledge Domains

The assistant covers:
- Policy types (Term, Whole, Universal, Variable)
- Benefits (Death benefit, cash value, living benefits)
- Eligibility (Age, health, occupation)
- Claims process and requirements
- Premium factors and cost optimization
- Policy management

## Configuration Options

Environment variables in `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | Required | OpenAI API key |
| `OPENAI_MODEL` | `gpt-4o-mini` | Model for chat |
| `EMBEDDING_MODEL` | `text-embedding-3-small` | Embedding model |
| `VECTOR_STORE_PATH` | `./data/vector_store` | FAISS index location |
| `TOP_K_RESULTS` | `3` | Retrieved context chunks |
| `API_HOST` | `0.0.0.0` | API server host |
| `API_PORT` | `8000` | API server port |

## Extending the Knowledge Base

Edit `app/knowledge_base/insurance_data.py` and rebuild the vector store:

```python
from app.vector_store.faiss_store import InsuranceVectorStore

store = InsuranceVectorStore()
store.rebuild_store()
```

## Project Structure

```
lisa-ai-agent-private/
├── app/
│   ├── agent/
│   │   └── insurance_agent.py       # LangGraph agent
│   ├── vector_store/
│   │   └── faiss_store.py           # FAISS implementation
│   ├── knowledge_base/
│   │   └── insurance_data.py        # Domain knowledge
│   ├── api/
│   │   └── server.py                # FastAPI server
│   └── cli/
│       └── chat_cli.py              # CLI interface
├── data/
│   └── vector_store/                # FAISS index (auto-generated)
├── diagrams/
├── video/
├── requirements.txt
├── .env.example
└── README.md
```

## Requirements

- Python 3.10+
- OpenAI API key
- Dependencies in `requirements.txt`

## AI usage

- Chat interface building
- Research about Life insurance
- Create a knowledge base with Chatgpt

## Evaluation criteria covered
- Handles life insurance queries accurately and
contextually (**50%**)
- Clean and readable code, modular, and scalable
design (**30%**)
- Clear setup guide and inline documentation (**10%**)
- Responsive and intuitive chat/voice interface (**5%**) covered only chat interface
