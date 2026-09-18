# Flask + Gemini + PostgreSQL RAG Chatbot

A document-grounded RAG chatbot using Flask, Gemini, and PostgreSQL with pgvector.

## Architecture

Document -> text extraction -> chunking -> Gemini embeddings -> PostgreSQL/pgvector
-> vector similarity retrieval -> grounded Gemini answer -> validator -> final response

The chatbot never sends the original document to Gemini during question answering. Only text chunks retrieved from PostgreSQL are supplied as evidence.

## Requirements

- Python 3.10+
- PostgreSQL 15+ with pgvector (the included Docker setup provides this)
- Gemini API key

## 1. Start PostgreSQL

```bash
docker compose up -d db
```

## 2. Create environment

Windows:
```powershell
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

Install:
```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set `GEMINI_API_KEY`.

## 3. Initialize database

```bash
python scripts/init_db.py
```

## 4. Run Flask

```bash
python run.py
```

Open http://127.0.0.1:5000

## 5. Upload documents

Use the Upload Document page. Supported formats in this starter are PDF, DOCX, TXT and Markdown.

The ingestion pipeline:
1. Extracts text locally.
2. Normalizes text.
3. Splits it into chunks with overlap.
4. Creates embeddings with Gemini's embedding API.
5. Stores document metadata, chunk text, and vectors in PostgreSQL.

## Hallucination controls

- Retrieval is mandatory before answer generation.
- Gemini is instructed to answer only from evidence returned from PostgreSQL.
- If evidence is insufficient, the model must say that the information is not available in the uploaded documents.
- The validator checks that every factual answer sentence has meaningful lexical support in retrieved evidence.
- The validator also rejects empty, malformed, or unsupported answers.
- Failed validation triggers one stricter regeneration attempt.
- If the second answer fails, the system returns a safe evidence-based fallback.

## Notes

The embedding model is accessed through Gemini's API; there is no local pretrained model or Ollama dependency.
