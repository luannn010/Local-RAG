# Local-RAG

Local-RAG is a Retrieval-Augmented Generation (RAG) system that enables you to chat with your own knowledge base using local files and vector search. It leverages Qdrant for vector storage, LangChain for orchestration, and supports both PostgreSQL and Redis for chat history management. The system is designed for extensibility and local-first privacy.

## Features

- **Chat with your notes and documents** using natural language queries.
- **Retrieval-Augmented Generation**: Combines LLMs with vector search for context-aware answers.
- **Qdrant vector store** for fast and scalable similarity search.
- **Pluggable history management**: Supports Redis for fast in-memory chat history and PostgreSQL for persistent storage.
- **Supports Markdown, TXT, PDF, and JSON files** as knowledge sources.
- **Customizable trigger detection** for when to use RAG vs. pure LLM chat.

## Folder Structure

```
src/
  embedder/         # Embedding logic (Ollama, etc.)
  history/          # Chat history management (Redis, Postgres, LangChain wrapper)
  preprocessor/     # File and folder loaders
  runner/           # Main RAG chat runner
  trigger/          # Trigger detection logic
  vectorstore/      # Qdrant vector store integration
main.py             # Entry point
.env                # Environment configuration
requirements.txt    # Python dependencies
```

## Quickstart

### 1. Clone the repository

```sh
git clone https://github.com/luannn010/Local-RAG.git
cd Local-RAG
```

### 2. Install dependencies

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment

Edit the `.env` file to match your setup. Example:

```env
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=qdrant-apikey
QDRANT_COLLECTION_NAME="obsidiant"
LLM_MODEL="mistral:7b"
DB_TYPE=postgres
DB_POSTGRESDB_HOST=postgres
DB_POSTGRESDB_PORT=5432
DB_POSTGRESDB_DATABASE=postgres
DB_POSTGRESDB_USER=user
DB_POSTGRESDB_PASSWORD=password
QUEUE_MODE=redis
QUEUE_REDIS_HOST=redis
```

- Make sure Qdrant, PostgreSQL, and Redis are running and accessible.

### 4. Run the application

```sh
python src/main.py
```

You should see:
```
🧠 Chat with your knowledge base (type 'exit' to quit)
Using collection: 'obsidiant'
```

Type your questions to interact with your knowledge base!

## Adding Knowledge

- Place your Markdown, TXT, PDF, or JSON files in a folder.
- Use the `FolderLoader` to ingest documents (see `src/preprocessor/folder_loader.py`).

## Development Notes

- Embeddings are generated using Ollama models (configurable via `.env`).
- Vector search is powered by Qdrant.
- Chat history is managed in Redis (for fast access) and flushed to PostgreSQL for persistence.
- Trigger detection determines when to use RAG vs. pure LLM chat (see `src/trigger/trigger_detector.py`).

## Troubleshooting

- **Database connection errors:** Ensure your `.env` matches your running services and credentials.
- **Qdrant errors:** Make sure Qdrant is running and the API key is correct.
- **Module import errors:** Activate your virtual environment and check your `PYTHONPATH`.

## License

MIT

---

**Made with ❤️ for local, private, and extensible AI-powered knowledge retrieval.**
