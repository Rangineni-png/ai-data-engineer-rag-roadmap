# Day 13 - Logging, Error Handling, and Data Quality Checks

## Today’s Goal

Improve the RAG API by adding logging, validation, error handling, and simple data quality checks.

Before Day 13, the RAG API could answer questions, but it did not have strong validation, logging, or error handling.

On Day 13, we made the system more reliable and production-like.

---

## Questions

### 1. Why is logging important in a production RAG system?

Logging is important because it helps developers understand what the system is doing.

In a production RAG system, logging helps track:

* when the API starts
* whether the model loaded successfully
* whether ChromaDB connected successfully
* what questions were asked
* whether retrieval was relevant
* which document was retrieved
* what errors happened
* whether invalid input was sent

Without logs, it is difficult to debug problems.

For example, if a user says the answer is wrong, logs can help check which document chunk was retrieved and whether the model generated the wrong answer.

---

### 2. What is the difference between a warning log and an error log?

A warning log means something unexpected happened, but the system can still continue.

Example:

```text
Question cannot be empty.
```

This is a warning because the user sent bad input, but the API itself is still working.

An error log means something failed and may need attention.

Example:

```text
Could not connect to Ollama. Make sure Ollama is running.
```

This is an error because the system cannot generate an LLM answer if Ollama is not available.

In simple words:

Warning = problem, but system can continue.
Error = failure that may stop part of the system.

---

### 3. Why do we validate raw documents before chunking?

We validate raw documents before chunking because bad documents can create bad chunks.

If a document is empty, too short, or unreadable, it should not be sent into the RAG pipeline.

Bad input documents can cause:

* useless chunks
* poor embeddings
* bad retrieval results
* incorrect answers
* wasted processing time

Document validation improves the quality of the knowledge base.

---

### 4. What does `validate_documents()` check?

`validate_documents()` checks whether the documents are usable before chunking.

It checks:

* whether any documents were loaded
* whether the cleaned document text is empty
* whether the document has too few words
* whether at least one valid document remains after validation

If a document is empty or too short, the function skips it and writes a warning log.

If no valid documents remain, it raises an error.

This prevents poor-quality documents from entering the vector database.

---

### 5. Why do we validate user questions before retrieval?

We validate user questions before retrieval so the system does not waste time processing bad input.

For example, these should not be sent to the RAG system:

```text
empty question
one-letter question
very long question
None/null question
```

If we do not validate questions, the system may create meaningless embeddings, retrieve poor chunks, or return confusing answers.

Question validation makes the API safer and cleaner.

---

### 6. What does `validate_question()` check?

`validate_question()` checks whether the user question is valid.

It checks:

* the question is not `None`
* the question is not empty
* the question is not too short
* the question is not too long

If the question is valid, it returns the cleaned question.

If the question is invalid, it raises a `ValueError`.

Example invalid question:

```json
{
  "question": ""
}
```

Expected API response:

```json
{
  "detail": "Question cannot be empty."
}
```

---

### 7. Why should an empty question return a 400 error instead of a 500 error?

An empty question should return a `400 Bad Request` error because the problem is caused by the user’s input.

A `500 Internal Server Error` means something failed inside the server.

For an empty question, the server is not broken. The request is invalid.

Correct behavior:

```text
Empty question → 400 Bad Request
Server crash → 500 Internal Server Error
```

This makes the API more professional and easier to debug.

---

### 8. What happens if Ollama is not running?

If Ollama is not running, the API cannot get an answer from the local LLM.

In Day 13, we added error handling so the system does not crash immediately.

Instead, it returns a clear message such as:

```text
Answer: The local LLM service is not available. Please make sure Ollama is running.
Sources: None
```

This is better than showing a confusing Python error.

It helps the user understand what went wrong and how to fix it.

---

### 9. What kind of information is saved in the log file?

The log file saves useful system events and debugging information.

Examples:

* API startup messages
* model loading messages
* ChromaDB connection messages
* document validation messages
* questions asked by users
* retrieval relevance status
* top source file
* top retrieval distance
* bad request warnings
* Ollama connection errors
* pipeline completion messages

The log file is saved here:

```text
04-rag-project/final_rag_pipeline/logs/rag_pipeline.log
```

This file helps debug the RAG pipeline and API behavior.

---

### 10. How does Day 13 make the project more production-like?

Day 13 makes the project more production-like because real systems need more than just correct answers.

They also need:

* logging
* validation
* error handling
* clear API error responses
* data quality checks
* debugging information
* safer behavior when something fails

Before Day 13, the system worked, but it was less reliable.

After Day 13, the system can handle bad inputs, missing/poor documents, Ollama issues, and API errors more professionally.

This is closer to how a real AI Data Engineering or AI Platform project should be built.

---

## Reflection

### What I completed:

I completed Day 13 by improving the RAG API with logging, input validation, document data quality checks, and better error handling. I added a log file, validated user questions, checked document quality before chunking, and handled Ollama connection issues more safely.

### What was easy:

Testing the `/health` endpoint and empty question validation was easy. The API correctly returned that the model and collection were loaded, and it returned an error message for an empty question.

### What was difficult:

Understanding why `uvicorn api:app --reload` kept restarting was difficult. The issue happened because the log file was being updated inside the project folder, and Uvicorn detected each log update as a file change. Running `uvicorn api:app` without `--reload` fixed the repeated reload problem.

### What I need to revise:

I need to revise logging levels, API status codes, validation errors, error handling, and the difference between retrieval quality and LLM generation quality.

I also need to remember that retrieval can be correct even if the small local LLM gives a weak answer. In that case, fallback logic can use the top retrieved chunk.

---

## Key Takeaway

Day 13 improved the reliability of the local RAG API.

The system now handles:

* valid questions
* empty questions
* document validation
* logging to a file
* Ollama connection issues
* weak LLM responses using fallback logic

The improved flow is:

User question
→ validate question
→ retrieve chunks from ChromaDB
→ check retrieval relevance
→ call Ollama
→ handle LLM/API errors
→ return answer with sources
→ save logs for debugging

This makes the RAG project more professional and closer to a production-ready AI system.
