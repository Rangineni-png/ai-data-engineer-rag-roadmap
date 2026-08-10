# Day 9 - Local RAG with Ollama

## Today’s Goal

Use Ollama as a local LLM to generate answers from retrieved ChromaDB context.

## Questions

### 1. What is Ollama?

Ollama is a tool that lets us run large language models locally on our own computer.

Instead of calling an external API, we can download a model such as `gemma3:1b` and use it through a local API.

In this project, Ollama acts as the local LLM used to generate answers from retrieved company policy context.

---

### 2. Why are we using a local LLM?

We are using a local LLM because it helps us build a private RAG system.

A local LLM can generate answers without sending company documents or user questions to an external service.

This is useful for:

- privacy
- learning local AI deployment
- testing RAG systems
- understanding how enterprise AI systems can work with private data

---

### 3. What role does ChromaDB play in Day 9?

ChromaDB acts as the retrieval layer.

It stores the document chunks, embeddings, and metadata. When the user asks a question, ChromaDB finds the most relevant chunks based on semantic similarity.

In Day 9, ChromaDB retrieves the context that Ollama will use to generate the final answer.

---

### 4. What role does Ollama play in Day 9?

Ollama acts as the answer generation layer.

After ChromaDB retrieves the relevant chunks, the retrieved context and user question are sent to Ollama.

Ollama then generates a natural language answer based on the provided context.

So:

ChromaDB retrieves the evidence.  
Ollama writes the answer.

---

### 5. What does `build_prompt()` do?

`build_prompt()` creates the instruction that is sent to Ollama.

It combines:

- system instructions
- retrieved context
- user question
- answer formatting rules

The prompt tells Ollama to answer only using the provided context and to include the source file name and chunk number.

---

### 6. Why do we instruct the LLM to use only the provided context?

We instruct the LLM to use only the provided context to reduce hallucination.

Without this instruction, the model may answer using outside knowledge or make up information.

In RAG systems, the answer should be grounded in the retrieved documents.

This is especially important for company policy, legal, healthcare, finance, or private enterprise data.

---

### 7. What does `call_ollama()` do?

`call_ollama()` sends the prompt to the local Ollama API.

It makes a POST request to:

`http://localhost:11434/api/generate`

The function sends:

- model name
- prompt
- stream setting

Then it receives the generated answer from Ollama and returns it to the Python script.

---

### 8. How is Day 9 different from Day 8?

Day 8 used a simple rule-based answer function. It mostly returned the best retrieved chunk as the answer.

Day 9 uses a real local LLM through Ollama.

Day 8:

Question  
→ retrieve chunks  
→ return best chunk as formatted answer

Day 9:

Question  
→ retrieve chunks  
→ build prompt  
→ send context to Ollama  
→ generate natural answer

So Day 9 is closer to a real RAG chatbot.

---

### 9. What are the benefits of local RAG?

Local RAG has several benefits:

- private documents stay on the local machine
- no external API key is required
- useful for learning and prototyping
- good for sensitive enterprise data experiments
- can work offline after models are downloaded
- gives control over the model and retrieval pipeline

The main limitation is that small local models may sometimes give weaker or less accurate answers than larger models.

---

### 10. What output file was created?

The output file created was:

`day9_ollama_rag_answers.csv`

It contains:

- question
- answer
- top_source_file
- top_chunk_id
- top_distance
- context

This file stores the questions, retrieved context, Ollama-generated answers, and source information.

## Reflection

What I completed:
I completed the Day 9 local RAG pipeline. I connected ChromaDB retrieval with Ollama, sent retrieved context to a local LLM, generated natural answers, and saved the results into `day9_ollama_rag_answers.csv`.

What was easy:
Running Ollama through the local API was easy after confirming that the API worked with `curl`.

What was difficult:
The small local model sometimes gave imperfect answers, such as failing to answer the password question even when the correct context was retrieved. I also learned that a missing comma in the question list can merge two questions into one string.

What I need to revise:
I need to revise prompt design, Ollama API calls, local LLM limitations, and the difference between retrieval quality and generation quality.