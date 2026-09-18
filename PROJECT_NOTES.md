# Project Notes

## Core rule
At question-answering time, the source document is NOT read. Retrieval uses embeddings and chunk text stored in PostgreSQL.

## Data model
- documents: uploaded file metadata
- document_chunks: chunk content + Gemini vector embedding + document reference

## Security / reliability ideas for the next iteration
- Add authentication before exposing the app publicly.
- Add upload virus scanning and stricter file validation for production.
- Add per-user document ownership.
- Add audit logs for questions, retrieved chunk IDs, and validator results.
- Add hybrid BM25/full-text + vector retrieval if the corpus becomes large.
