# Day 7 - Retrieval Pipeline for RAG

## Today’s Goal

Build a reusable retrieval pipeline that takes user questions and retrieves relevant chunks from ChromaDB.

## Questions

### 1. What is retrieval in RAG?

Retrieval is the step where the system searches the vector database and finds the most relevant document chunks for a user question.

In our project, retrieval means:

User question  
→ convert question into embedding  
→ search ChromaDB  
→ return top matching chunks

Retrieval is the “R” in RAG.

---

### 2. What is the role of the user question in retrieval?

The user question is the input used to search the vector database.

For example:

“How many days can employees work remotely?”

The system uses this question to find the most relevant stored chunks. The question is converted into an embedding and compared with the embeddings stored in ChromaDB.

---

### 3. Why do we convert the user question into an embedding?

We convert the user question into an embedding so the system can compare the meaning of the question with the meaning of stored document chunks.

Text cannot be directly compared by meaning, so both the question and document chunks are converted into vectors.

Then ChromaDB compares:

question embedding  
vs  
stored chunk embeddings

---

### 4. What does ChromaDB compare during retrieval?

ChromaDB compares the user question embedding with the stored chunk embeddings.

It checks which chunks are closest in meaning to the question.

Example:

Question:

“How many days can employees work remotely?”

Best matching chunk:

remote_work_policy_chunk_1

This happened because the remote work chunk contains information about employees working remotely up to three days per week.

---

### 5. What does `top_k` mean?

`top_k` means how many top matching chunks we want to retrieve.

If:

```python
top_k = 3