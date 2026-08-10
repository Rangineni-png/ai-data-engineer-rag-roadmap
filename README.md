
# AI Data Engineer RAG Pipeline

## Project Overview

This project is a local Retrieval-Augmented Generation system built for company policy question answering.

It demonstrates how raw company documents can be transformed into an AI-ready knowledge base using document processing, chunking, embeddings, vector search, and local LLM answer generation.

The system uses ChromaDB for vector storage, Sentence Transformers for embeddings, Ollama for local LLM generation, and FastAPI for serving answers through an API.

---

## Role Focus

This project demonstrates skills for roles such as:

- AI Data Engineer
- GenAI Data Engineer
- RAG Data Engineer
- LLM Data Engineer
- AI/ML Data Engineer
- AI Platform Engineer
- ML Infrastructure Engineer

---

## Problem Statement

Companies often have important knowledge stored in unstructured documents such as policy files, internal guides, PDFs, manuals, and support documents.

Traditional search may not understand meaning well, and LLMs may hallucinate if they do not have access to the correct company knowledge.

This project solves that problem by building a RAG pipeline that retrieves relevant document chunks before generating an answer.

---

## Project Architecture

```text
Raw Documents
    ↓
Text Cleaning
    ↓
Document Chunking
    ↓
Embedding Generation
    ↓
ChromaDB Vector Database
    ↓
Semantic Retrieval
    ↓
Context Building
    ↓
Ollama Local LLM
    ↓
FastAPI Response with Sources
````

---

## Features

* Loads raw text documents
* Cleans document text
* Splits documents into overlapping chunks
* Creates embeddings using Sentence Transformers
* Stores chunks, embeddings, and metadata in ChromaDB
* Retrieves relevant chunks using semantic search
* Generates answers using a local Ollama model
* Returns source citations
* Handles unknown questions
* Provides FastAPI endpoints
* Adds logging, validation, and error handling
* Includes fallback logic when the local LLM gives a weak response

---

## Tech Stack

| Category        | Tools                 |
| --------------- | --------------------- |
| Programming     | Python                |
| Data Processing | pandas                |
| Embeddings      | sentence-transformers |
| Vector Database | ChromaDB              |
| Local LLM       | Ollama                |
| API Framework   | FastAPI               |
| API Server      | Uvicorn               |
| Testing         | curl, Swagger UI      |
| Version Control | Git, GitHub           |

---

## Project Structure

```text
AI-Data-Engineer/
├── 01-sql-practice/
├── 02-python-practice/
├── 03-data-engineering/
├── 04-rag-project/
│   └── final_rag_pipeline/
│       ├── api.py
│       ├── rag_pipeline.py
│       ├── data/
│       │   ├── raw_documents/
│       │   ├── cleaned_documents/
│       │   └── output/
│       ├── vector_db/
│       └── logs/
├── 05-notes/
├── 06-resume/
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Final RAG Pipeline Location

The main portfolio-ready project is located here:

```text
04-rag-project/final_rag_pipeline/
```

Main files:

```text
rag_pipeline.py
api.py
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd AI-Data-Engineer
```

### 2. Create and activate a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Mac/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Install and start Ollama

Install Ollama and pull the model used in this project:

```bash
ollama pull gemma3:1b
```

Make sure Ollama is running locally.

---

## How to Run the RAG Pipeline Script

Go to the final pipeline folder:

```bash
cd 04-rag-project/final_rag_pipeline
```

Run:

```bash
python rag_pipeline.py
```

This will:

* load raw documents
* clean text
* create chunks
* create embeddings
* build ChromaDB vector database
* answer sample questions
* save results to CSV

---

## How to Run the FastAPI Server

From the final pipeline folder:

```bash
cd 04-rag-project/final_rag_pipeline
```

Run:

```bash
uvicorn api:app
```

The API will start at:

```text
http://127.0.0.1:8000
```

---

## API Endpoints

### Root Endpoint

```http
GET /
```

Returns basic API information.

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "ok",
  "model_loaded": true,
  "collection_loaded": true
}
```

### Ask a Question

```http
POST /ask
```

Example request:

```json
{
  "question": "How many days can employees work remotely?"
}
```

Example response:

```json
{
  "question": "How many days can employees work remotely?",
  "answer": "Employees may work remotely up to three days per week with manager approval.",
  "retrieval_relevant": true,
  "top_source_file": "remote_work_policy.txt",
  "top_chunk_id": "remote_work_policy_chunk_1",
  "top_distance": 0.47,
  "sources": "remote_work_policy.txt#chunk-1"
}
```

---

## Testing with curl

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Known question:

```bash
curl -X POST "http://127.0.0.1:8000/ask" -H "Content-Type: application/json" -d "{\"question\":\"Can employees share passwords?\"}"
```

Unknown question:

```bash
curl -X POST "http://127.0.0.1:8000/ask" -H "Content-Type: application/json" -d "{\"question\":\"What is my name?\"}"
```

Empty question validation:

```bash
curl -X POST "http://127.0.0.1:8000/ask" -H "Content-Type: application/json" -d "{\"question\":\"\"}"
```

Expected empty question response:

```json
{
  "detail": "Question cannot be empty."
}
```

---

## Example Questions

The system can answer questions such as:

* How many days can employees work remotely?
* Can employees share passwords?
* How many vacation days do full-time employees receive?
* Where should suspicious emails be reported?

If the answer is not found in the documents, the system should return a not-found response instead of guessing.

---

## Data Engineering Contributions

This project includes several AI Data Engineering tasks:

* raw document ingestion
* text cleaning
* metadata creation
* chunking strategy
* embedding generation
* vector database storage
* semantic retrieval
* source tracking
* data quality checks
* logging
* reproducible pipeline design

---

## AI Application Contributions

This project also includes AI application development tasks:

* prompt design
* local LLM integration
* answer generation
* citation formatting
* FastAPI endpoint development
* request and response validation
* API testing

---

## Key Learning Outcomes

Through this project, I learned how to:

* process unstructured text documents
* prepare documents for RAG
* create embeddings
* store embeddings in a vector database
* perform semantic search
* connect retrieval with local LLM generation
* build an API around a RAG pipeline
* add logging and validation
* explain an end-to-end GenAI data pipeline

---

## Future Improvements

Possible future improvements:

* add PDF ingestion
* add cloud storage such as AWS S3
* add Airflow orchestration
* add database ingestion
* add hybrid search
* add reranking
* add better evaluation metrics
* add Docker support
* deploy the API
* add authentication
* add Streamlit or React frontend
* improve citations with page numbers
* use stronger local or cloud LLMs

---

## Resume Summary

Built an end-to-end local RAG pipeline for company policy question answering using Python, ChromaDB, Sentence Transformers, Ollama, and FastAPI. Implemented document ingestion, text cleaning, chunking, embedding generation, semantic retrieval, source-grounded answer generation, API endpoints, validation, logging, and error handling.

---

## Status

Current status: functional local RAG API with logging, validation, semantic retrieval, local LLM generation, and source citations.

````

After pasting, save with:

```text
Ctrl + S
````

Then create `requirements.txt` in the project root and add:

```txt
pandas
requests
chromadb
sentence-transformers
fastapi
uvicorn
pydantic
```
