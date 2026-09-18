import os
import tempfile
from pathlib import Path
from flask import Blueprint, jsonify, render_template, request
from .services import answer_question, ingest_document

main_bp = Blueprint("main", __name__)
ALLOWED = {".pdf", ".docx", ".txt", ".md"}

@main_bp.get("/")
def index():
    return render_template("index.html")

@main_bp.post("/upload")
def upload():
    file = request.files.get("file")
    if not file or not file.filename:
        return jsonify({"error": "Select a document first."}), 400
    suffix = Path(file.filename).suffix.lower()
    if suffix not in ALLOWED:
        return jsonify({"error": "Supported formats: PDF, DOCX, TXT, MD."}), 400
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        file.save(tmp.name)
        temp_path = tmp.name
    try:
        doc_id, count = ingest_document(temp_path, Path(file.filename).name)
        return jsonify({"message": "Document indexed successfully.", "document_id": doc_id, "chunks": count})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500
    finally:
        try:
            os.remove(temp_path)
        except OSError:
            pass

@main_bp.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    question = (data.get("question") or "").strip()
    if not question:
        return jsonify({"error": "Question is required."}), 400
    try:
        return jsonify(answer_question(question))
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500
