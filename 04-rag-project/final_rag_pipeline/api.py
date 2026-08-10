import logging
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from rag_pipeline import (
    build_knowledge_base,
    connect_to_existing_collection,
    answer_question
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


app = FastAPI(
    title="Local RAG API",
    description="A local Retrieval-Augmented Generation API using ChromaDB and Ollama.",
    version="1.0.0"
)


model = None
collection = None


class QuestionRequest(BaseModel):
    question: str


class RAGResponse(BaseModel):
    question: str
    answer: str
    retrieval_relevant: bool
    top_source_file: Optional[str]
    top_chunk_id: Optional[str]
    top_distance: Optional[float]
    sources: str


@app.on_event("startup")
def startup_event():
    """
    Load the embedding model and connect to ChromaDB when the API starts.
    If the vector database does not exist yet, build the knowledge base first.
    """
    global model, collection

    try:
        logging.info("Starting RAG API")

        try:
            model, collection = connect_to_existing_collection()
            logging.info("Connected to existing knowledge base")

        except Exception:
            logging.warning("Existing knowledge base not found. Building knowledge base.")
            model, collection = build_knowledge_base()
            logging.info("Knowledge base built successfully")

    except Exception as e:
        logging.error(f"Startup failed: {e}")
        raise


@app.get("/")
def root():
    return {
        "message": "Local RAG API is running",
        "endpoints": {
            "ask": "/ask",
            "health": "/health",
            "docs": "/docs"
        }
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "collection_loaded": collection is not None
    }


@app.post("/ask", response_model=RAGResponse)
def ask_question(request: QuestionRequest):
    global model, collection

    if model is None or collection is None:
        raise HTTPException(
            status_code=500,
            detail="RAG system is not initialized."
        )

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:
        result = answer_question(
            question=request.question,
            model=model,
            collection=collection
        )

        return {
            "question": result["question"],
            "answer": result["answer"],
            "retrieval_relevant": result["retrieval_relevant"],
            "top_source_file": result["top_source_file"],
            "top_chunk_id": result["top_chunk_id"],
            "top_distance": result["top_distance"],
            "sources": result["sources"]
        }

    except Exception as e:
        logging.error(f"Error answering question: {e}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )