# Day 4 - Chunking Documents for RAG

## Today’s Goal

Split cleaned documents into smaller chunks and save them with metadata.

## Questions

### 1. What is chunking?

Chunking is the process of splitting a large document into smaller pieces of text.

Instead of sending one full document to the AI system, we divide it into smaller chunks so each chunk can be processed, embedded, stored, and retrieved more easily.

Example:

Full document
→ chunk 1
→ chunk 2
→ chunk 3

---

### 2. Why do we chunk documents before creating embeddings?

We chunk documents before creating embeddings because embeddings work better on smaller, meaningful pieces of text.

If we create one embedding for an entire long document, the meaning becomes too broad. But if we create embeddings for smaller chunks, the vector database can retrieve the most relevant part of the document.

Simple rule:

Large document → too much information in one embedding
Smaller chunks → better semantic search and better retrieval

---

### 3. What is chunk size?

Chunk size is the amount of text allowed in each chunk.

In our script, we used word-based chunking:

```python
CHUNK_SIZE = 40
```

This means each chunk has around 40 words.

A small chunk may be more specific, but it may lose context.
A large chunk may preserve more context, but it may become less precise.

---

### 4. What is chunk overlap?

Chunk overlap means repeating some words from the previous chunk in the next chunk.

In our script, we used:

```python
CHUNK_OVERLAP = 10
```

This means each new chunk overlaps with the previous chunk by 10 words.

Overlap helps preserve context between chunks. Without overlap, important meaning may be split across two chunks and lost during retrieval.

---

### 5. Why do we need `chunk_id`?

We need `chunk_id` to uniquely identify each chunk.

Every chunk should have its own ID so we can track, search, update, debug, and cite it later.

Example:

```text
company_policy_chunk_1
company_policy_chunk_2
remote_work_policy_chunk_1
```

In RAG systems, `chunk_id` helps us know exactly which chunk was retrieved and used for the LLM answer.

---

### 6. Why do we keep `file_name` in every chunk?

We keep `file_name` in every chunk so we know which original document the chunk came from.

This is important for citations and traceability.

Example:

If the AI answers a question about leave policy, we can show that the answer came from:

```text
company_policy.txt
```

Without `file_name`, we would not know the source of the retrieved information.

---

### 7. What columns were created in `document_chunks.csv`?

The `document_chunks.csv` file contains chunk-level information.

The columns created were:

* chunk_id
* file_name
* source_type
* chunk_number
* chunk_text
* word_count
* processed_at

These columns help track each chunk, its source document, its text, its size, and when it was processed.

---

### 8. How does chunking help semantic search?

Chunking helps semantic search by making each searchable unit smaller and more focused.

When a user asks a question, the vector database compares the question with individual chunks instead of the entire document. This helps retrieve the most relevant section.

Example:

User question:

```text
How many days can employees work remotely?
```

The system can retrieve the specific chunk from `remote_work_policy.txt` that talks about remote work days.

This improves retrieval accuracy.

---

### 9. How will these chunks connect to embeddings later?

Each chunk will be converted into an embedding, which is a numerical vector representation of the chunk’s meaning.

The next pipeline will look like this:

```text
document_chunks.csv
→ take chunk_text
→ create embeddings
→ store embeddings with chunk_id and file_name
→ search similar chunks using a user question
```

So the chunks created today are the direct input for the embedding and vector database stages.

## Reflection

What I completed:
I completed the Day 4 chunking pipeline. I read cleaned documents, split them into word-based chunks, created chunk metadata, and saved the results into `document_chunks.csv`.

What was easy:
Running the script and creating the output file was easy.

What was difficult:
Understanding chunk size and chunk overlap was slightly difficult because they affect how much context each chunk contains.

What I need to revise:
I need to revise chunk size, chunk overlap, chunk metadata, and how chunks are later converted into embeddings for vector search.
