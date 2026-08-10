# Day 12 - FastAPI Endpoint for RAG

## Today’s Goal

Turn the final RAG pipeline into an API using FastAPI.

Before Day 12, the RAG system worked as a Python script. Questions were written inside the script and answers were printed in the terminal.

On Day 12, the RAG system was exposed through an API so a user or another application can send a question and receive a JSON response.

---

## Questions

### 1. What is FastAPI?

FastAPI is a Python framework used to build APIs.

It allows us to create endpoints such as:

* `/`
* `/health`
* `/ask`

These endpoints allow users or applications to interact with the RAG system through HTTP requests.

In this project, FastAPI helps turn the local RAG pipeline into a service.

---

### 2. Why do we need an API for a RAG system?

We need an API so other applications can use the RAG system without manually running a Python script.

Before the API, questions were hardcoded inside `rag_pipeline.py`.

With the API, a user can send a question like this:

```json
{
  "question": "How many days can employees work remotely?"
}
```

The API sends the question to the RAG pipeline and returns the answer as JSON.

This is closer to how real AI applications work.

---

### 3. What does the `/ask` endpoint do?

The `/ask` endpoint receives a user question and returns a RAG-generated answer.

It performs this flow:

User question
→ FastAPI receives request
→ RAG pipeline retrieves relevant chunks from ChromaDB
→ retrieved context is sent to Ollama
→ Ollama generates an answer
→ API returns answer with source information

The `/ask` endpoint is the main endpoint of the RAG API.

---

### 4. What does the `/health` endpoint do?

The `/health` endpoint checks whether the API is running properly.

It returns information such as:

* API status
* whether the embedding model is loaded
* whether the ChromaDB collection is loaded

Example response:

```json
{
  "status": "ok",
  "model_loaded": true,
  "collection_loaded": true
}
```

This is useful for debugging and monitoring.

---

### 5. Why do we load the model and collection at startup?

We load the embedding model and ChromaDB collection at startup so they are ready before users send questions.

The embedding model can take time to load. If we loaded it for every request, the API would be slow.

Better approach:

API starts
→ load embedding model once
→ connect to ChromaDB once
→ reuse them for all questions

This makes the API faster and more production-like.

---

### 6. What is the request body for `/ask`?

The request body for `/ask` is JSON.

Example:

```json
{
  "question": "How many days can employees work remotely?"
}
```

The request must contain a `question` field.

If the question is empty, the API should return an error because the RAG system needs a valid question to search the vector database.

---

### 7. What is the response body from `/ask`?

The response from `/ask` contains the answer and retrieval information.

It includes:

* `question`
* `answer`
* `retrieval_relevant`
* `top_source_file`
* `top_chunk_id`
* `top_distance`
* `sources`

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

This response is useful because it gives both the answer and the source information.

---

### 8. How is Day 12 different from Day 11?

Day 11 created the final integrated RAG pipeline as a Python script.

Day 11 flow:

Run script
→ hardcoded questions
→ answers printed in terminal

Day 12 turned that pipeline into an API.

Day 12 flow:

Start FastAPI server
→ send question to `/ask` endpoint
→ receive answer as JSON

The main difference is that Day 12 makes the RAG system usable by other applications.

---

### 9. How does this make the project more production-like?

FastAPI makes the project more production-like because real AI systems are usually exposed as APIs.

A frontend app, chatbot, internal company tool, or another backend service can call the API.

Production-like features added on Day 12:

* API endpoint for asking questions
* JSON request and response
* health check endpoint
* startup loading of model and collection
* error handling for empty questions
* automatic API documentation through `/docs`

This is an important step from “local script” to “usable AI service.”

---

### 10. What can be improved next?

Next improvements include:

* better error handling
* request logging
* API response formatting
* better citation formatting
* data quality checks
* modular code structure
* environment variables for model names and paths
* testing with more documents
* adding PDF support
* deployment preparation
* creating a clean README
* adding example API requests and responses

The next major step is to make the API more reliable and professional.

---

## Reflection

### What I completed:

I completed Day 12 by creating a FastAPI API for the local RAG system. I added endpoints for `/`, `/health`, and `/ask`. I connected the API to the existing RAG pipeline so users can send questions and receive answers as JSON.

### What was easy:

Creating the API file and starting the FastAPI server was understandable because it reused the final RAG pipeline from Day 11.

### What was difficult:

Understanding that the API server must keep running in one terminal while testing requests from another terminal was new. It was also important to understand the difference between opening the browser and keeping the backend server running.

### What I need to revise:

I need to revise FastAPI endpoints, request bodies, response bodies, startup events, API testing with Swagger UI, and testing endpoints using `curl`.

---

## Key Takeaway

Day 12 turned the local RAG pipeline into an API.

The new flow is:

User or application
→ sends question to `/ask`
→ FastAPI receives request
→ ChromaDB retrieves relevant chunks
→ Ollama generates answer
→ API returns answer and sources as JSON

This makes the RAG project closer to a real AI engineering application.
