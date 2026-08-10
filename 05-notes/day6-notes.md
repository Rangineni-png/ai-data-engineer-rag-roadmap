# Day 6 - Vector Database with ChromaDB

## Today’s Goal

Store document chunks and embeddings in ChromaDB and run vector similarity search.

## Questions

### 1. What is a vector database?

A vector database is a database designed to store embeddings and search them by similarity.

Instead of searching only exact keywords, a vector database searches based on meaning. It stores vector representations of text, images, or other data and helps retrieve the most relevant items for a user query.

In RAG systems, vector databases are used to find the most relevant document chunks for a question.

---

### 2. Why do we need a vector database instead of only saving embeddings in a `.npy` file?

A `.npy` file can store embeddings, but it is just a file of numerical arrays. It does not provide full database features.

A vector database helps us:

* store embeddings
* store text documents
* store metadata
* search similar vectors
* persist data locally
* manage collections
* retrieve source information
* scale better than manual NumPy search

In Day 5, we manually searched embeddings using NumPy. In Day 6, ChromaDB handled storage and similarity search like a real vector database.

---

### 3. What is ChromaDB?

ChromaDB is a local vector database used to store embeddings, documents, and metadata.

It is commonly used for RAG projects because it is simple to set up, runs locally, and supports similarity search over text chunks.

In this project, ChromaDB stored our company policy document chunks and allowed us to retrieve the most relevant chunk for a user query.

---

### 4. What is a collection in ChromaDB?

A collection in ChromaDB is like a table or container that stores related documents, embeddings, and metadata.

In our script, the collection name was:

company_policy_chunks

This collection stored all chunks from the company policy, IT security policy, and remote work policy documents.

---

### 5. What did we store in ChromaDB?

We stored four main things in ChromaDB:

* ids
* documents
* metadatas
* embeddings

The ids uniquely identify each chunk.
The documents store the actual chunk text.
The metadata stores source information like file name, chunk number, and word count.
The embeddings store the numerical vector representation of each chunk.

---

### 6. What are ids, documents, metadatas, and embeddings?

**ids:**
Unique identifiers for each chunk.

Example:

remote_work_policy_chunk_1

**documents:**
The actual text content of each chunk.

Example:

Employees may work remotely up to three days per week...

**metadatas:**
Extra information about each chunk.

Example:

file_name, chunk_number, word_count

**embeddings:**
Numerical vector representations of the chunk text. These vectors are used for similarity search.

---

### 7. What does similarity search do?

Similarity search finds the stored chunks whose embeddings are closest to the user query embedding.

In simple terms, it finds the chunks that are most similar in meaning to the question.

Example query:

How many days can employees work remotely?

The top result came from:

remote_work_policy.txt

This means the vector database correctly found the chunk related to remote work.

---

### 8. What is the difference between semantic search in Day 5 and ChromaDB search in Day 6?

In Day 5, we created embeddings and manually calculated similarity using NumPy dot product.

In Day 6, we stored chunks, metadata, and embeddings in ChromaDB and used ChromaDB to perform vector similarity search.

Day 5 was manual semantic search.
Day 6 was database-powered semantic search.

Day 6 is closer to how real RAG systems work.

---

### 9. Why is metadata important in vector database search?

Metadata is important because it tells us where the retrieved chunk came from.

For example, if ChromaDB retrieves a chunk, metadata tells us:

* file name
* chunk number
* word count
* source document

This is important for citations, debugging, filtering, and trust.

Without metadata, the system may retrieve useful text, but we would not know its source.

---

### 10. How will this connect to RAG answer generation later?

The vector database will become the retrieval layer of the RAG system.

Later, when a user asks a question:

1. The question will be converted into an embedding.
2. ChromaDB will search for similar chunks.
3. The top chunks will be retrieved.
4. The retrieved chunks will be sent to an LLM as context.
5. The LLM will generate an answer based on the retrieved chunks.
6. The answer will include source citations using metadata.

Full flow:

User question
→ query embedding
→ ChromaDB search
→ retrieve relevant chunks
→ send context to LLM
→ generate answer with citations

## Reflection

What I completed:
I completed the Day 6 vector database pipeline. I stored 6 document chunks with embeddings and metadata in ChromaDB, ran a similarity search, and saved the search results to `day6_search_results.csv`.

What was easy:
Running the script was easier after fixing the missing package issue. Seeing the correct remote work policy result was clear.

What was difficult:
Understanding the difference between saving embeddings in a file and storing them in a vector database was slightly difficult.

What I need to revise:
I need to revise ChromaDB collections, embeddings, metadata, similarity search, and how this retrieval layer connects to RAG answer generation.
