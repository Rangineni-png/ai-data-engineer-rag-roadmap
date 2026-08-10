# Day 5 - Embeddings for RAG

## Today’s Goal

Convert document chunks into embeddings and test semantic search.

## Questions

### 1. What are embeddings?

Embeddings are numerical vector representations of text. They convert text into lists of numbers that capture the meaning of the text.

For example, a sentence like:

"Employees may work remotely up to three days per week"

is converted into a vector like:

[0.12, -0.04, 0.33, ...]

These numbers help computers compare text by meaning instead of exact words.

---

### 2. Why do we create embeddings from chunks instead of full documents?

We create embeddings from chunks because smaller chunks are more specific and easier to retrieve.

If we create one embedding for a full document, the meaning becomes too broad. If we create embeddings for smaller chunks, the vector search can find the exact relevant part of the document.

Chunk-level embeddings improve retrieval accuracy in RAG systems.

---

### 3. What embedding model did we use?

We used this embedding model:

sentence-transformers/all-MiniLM-L6-v2

This model converts each chunk of text into a numerical embedding vector.

---

### 4. What does embedding dimension mean?

Embedding dimension means the number of values in each embedding vector.

In our output, the embedding shape was:

(6, 384)

This means each chunk was converted into a vector with 384 numbers.

So the embedding dimension is 384.

---

### 5. What does the shape of the embeddings array mean?

The embeddings shape was:

(6, 384)

This means:

* 6 = number of chunks
* 384 = number of dimensions in each embedding

So we created embeddings for 6 document chunks, and each chunk has a 384-dimensional vector.

---

### 6. Why did we save embeddings as a `.npy` file?

We saved embeddings as a `.npy` file because embeddings are numerical arrays, and `.npy` is an efficient format for saving NumPy arrays.

The file created was:

chunk_embeddings.npy

This file stores the actual vector values for all document chunks.

---

### 7. Why did we save chunk metadata separately?

We saved chunk metadata separately because embeddings only contain numbers. Metadata helps us understand what each vector belongs to.

The metadata includes useful information such as:

* chunk_id
* file_name
* chunk_text
* word_count
* embedding_model
* embedding_dimension

This helps us trace each embedding back to the original document and chunk.

---

### 8. What is semantic search?

Semantic search means searching by meaning instead of exact keywords.

For example, the query:

"How many days can employees work remotely?"

matched the remote work policy chunk even though the exact wording may not be identical.

Semantic search uses embeddings to compare the meaning of the user query with the meaning of stored chunks.

---

### 9. How did the query match the correct document chunk?

The query was converted into an embedding vector. Then the system compared that query vector with the stored chunk embeddings.

The most similar chunk received the highest similarity score.

In our result, the top match came from:

remote_work_policy.txt

This was correct because the query was about remote work days, and the remote work policy chunk contained information about employees working remotely up to three days per week.

---

### 10. How will these embeddings connect to a vector database later?

The embeddings we created today will later be stored inside a vector database.

The vector database will store:

* chunk embeddings
* chunk text
* chunk_id
* file_name
* metadata

Later, when a user asks a question, the system will create an embedding for the question and search the vector database for the most similar chunks.

Full flow:

User question
→ query embedding
→ vector database search
→ retrieve relevant chunks
→ send chunks to LLM
→ generate answer with citations

## Reflection

What I completed:
I completed the Day 5 embeddings pipeline. I created embeddings for document chunks, saved the embeddings as a `.npy` file, saved chunk metadata, and tested semantic search.

What was easy:
Running the script and seeing the semantic search results was easy after fixing the package installation issue.

What was difficult:
Understanding the embedding shape and how vectors represent meaning was a little difficult.

What I need to revise:
I need to revise embeddings, embedding dimensions, semantic search, and how embeddings connect to vector databases.
