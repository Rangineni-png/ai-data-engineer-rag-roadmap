Paste this as your complete `05-notes/day11-notes.md`.

# Day 11 - Final Integrated RAG Pipeline

## Today’s Goal

Combine document processing, chunking, vector database storage, retrieval, Ollama answer generation, citations, and not-found handling into one clean pipeline.

---

## Questions

### 1. Why did we combine all previous day-wise scripts into one final pipeline?

We combined all previous scripts into one final pipeline to make the project cleaner, reusable, and portfolio-ready.

Before Day 11, each step was separate:

* Day 3: document processing
* Day 4: chunking
* Day 5: embeddings
* Day 6: ChromaDB vector database
* Day 7: retrieval
* Day 8: simple answer generation
* Day 9: Ollama local LLM
* Day 10: improved prompt, citations, and not-found handling

On Day 11, we combined these steps into one organized script called `rag_pipeline.py`.

This makes the project look more like a real AI Data Engineering project instead of only daily practice files.

---

### 2. What does `build_knowledge_base()` do?

`build_knowledge_base()` builds the searchable knowledge base from raw documents.

It performs these steps:

1. Loads raw documents from the `raw_documents` folder.
2. Cleans the document text.
3. Saves cleaned documents.
4. Splits cleaned text into chunks.
5. Loads the embedding model.
6. Creates a ChromaDB collection.
7. Converts chunks into embeddings.
8. Stores chunks, embeddings, and metadata in ChromaDB.

In simple words:

`build_knowledge_base()` prepares the company documents so they can be searched by the RAG system.

---

### 3. What does `answer_question()` do?

`answer_question()` takes a user question and generates a source-grounded answer.

It performs these steps:

1. Converts the user question into an embedding.
2. Searches ChromaDB for the most relevant chunks.
3. Checks whether retrieval is relevant enough.
4. Builds context from retrieved chunks.
5. Builds a prompt using the question and context.
6. Sends the prompt to Ollama.
7. Gets the generated answer.
8. Returns the answer with source information.

In simple words:

`answer_question()` uses the prepared knowledge base to answer a user’s question.

---

### 4. What is the difference between building the knowledge base and answering questions?

Building the knowledge base is the preparation step. Answering questions is the usage step.

Building the knowledge base:

Raw documents
→ clean text
→ chunk text
→ create embeddings
→ store in ChromaDB

Answering questions:

User question
→ retrieve relevant chunks
→ build context
→ send to Ollama
→ generate answer with sources

In production, the knowledge base is usually built or updated only when documents change. Question answering happens many times when users interact with the system.

---

### 5. Why should the vector database not be rebuilt for every user question in production?

The vector database should not be rebuilt for every user question because rebuilding is expensive and unnecessary.

Rebuilding includes:

* reading all documents again
* cleaning text again
* chunking again
* creating embeddings again
* storing everything again in ChromaDB

This takes time and computing resources.

In production, the vector database should be built once and reused for many user questions. It should only be rebuilt or updated when new documents are added, existing documents are changed, or old documents are removed.

Correct production pattern:

Build/update knowledge base occasionally.
Answer user questions many times.

---

### 6. What files were created in the final pipeline?

The final pipeline created these files and folders:

* `rag_pipeline.py`
* `data/raw_documents/`
* `data/cleaned_documents/`
* `data/output/document_metadata.csv`
* `data/output/document_chunks.csv`
* `data/output/final_rag_results.csv`
* `vector_db/`

`rag_pipeline.py` contains the full integrated RAG pipeline.

`data/raw_documents/` stores the original company policy text files.

`data/cleaned_documents/` stores cleaned versions of the documents.

`document_metadata.csv` stores document-level metadata.

`document_chunks.csv` stores chunk-level data.

`final_rag_results.csv` stores the final questions, answers, sources, context, and retrieval information.

`vector_db/` stores the local ChromaDB vector database.

---

### 7. How does this final pipeline represent a complete RAG system?

This final pipeline represents a complete RAG system because it includes all major RAG stages.

The full flow is:

Documents
→ text cleaning
→ chunking
→ embeddings
→ vector database
→ retrieval
→ context building
→ LLM answer generation
→ citations
→ not-found handling

The system can answer questions using the company policy documents instead of relying only on the LLM’s memory.

This is the core idea of Retrieval-Augmented Generation:

Retrieve relevant information first, then generate an answer using that information.

---

### 8. Which parts of this pipeline belong to AI Data Engineering?

The AI Data Engineering parts are:

* loading raw documents
* cleaning document text
* creating document metadata
* chunking documents
* generating embeddings
* storing embeddings in ChromaDB
* managing chunk metadata
* building the vector database
* checking retrieval quality
* saving pipeline outputs
* organizing data folders
* making the pipeline reproducible

These tasks focus on preparing, storing, validating, and retrieving AI-ready data.

This is the core responsibility of an AI Data Engineer.

---

### 9. Which parts belong to AI application development?

The AI application development parts are:

* building the prompt
* calling Ollama
* generating the final answer
* formatting the answer
* showing sources to the user
* handling user questions
* creating a future API or chatbot interface

These tasks focus on how users interact with the AI system.

AI Data Engineering prepares the knowledge and retrieval layer. AI application development builds the user-facing answer experience.

---

### 10. What can be improved next?

The next improvements are:

* separate the project into cleaner modules
* add a FastAPI endpoint
* improve prompt quality
* improve citation formatting
* add better not-found detection
* add PDF ingestion
* add larger documents
* add better chunking strategy
* add document update logic
* add logging and error handling
* add tests
* add README documentation
* add architecture diagram
* prepare resume bullets
* prepare interview explanation

The biggest next step is to turn the pipeline into an API so a user can ask questions through an endpoint.

---

## Reflection

### What I completed:

I completed the Day 11 final integrated RAG pipeline. I combined document processing, text cleaning, chunking, embeddings, ChromaDB vector storage, retrieval, Ollama answer generation, citations, and not-found handling into one clean script.

### What was easy:

The previous day-wise scripts made it easier to understand the final pipeline because each part had already been practiced separately.

### What was difficult:

Understanding how all the separate parts connect into one complete RAG system was slightly difficult. The difference between building the knowledge base and answering questions is important and needs revision.

### What I need to revise:

I need to revise the full RAG flow, especially the difference between ingestion, chunking, embeddings, vector storage, retrieval, prompt building, answer generation, and citations.

---

## Key Takeaway

Day 11 changed the project from separate learning exercises into a portfolio-style RAG pipeline.

The final system now follows this flow:

Raw documents
→ clean text
→ create chunks
→ generate embeddings
→ store in ChromaDB
→ retrieve relevant chunks
→ send context to Ollama
→ generate source-grounded answers
