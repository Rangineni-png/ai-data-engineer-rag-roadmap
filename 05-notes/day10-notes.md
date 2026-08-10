# Day 10 - Improved RAG: Prompt, Citations, and Not Found Handling

## Today’s Goal

Improve the local RAG pipeline with better prompts, citations, and safer handling for unknown questions.

## Questions

### 1. Why did we improve the Day 9 prompt?

We improved the Day 9 prompt because the local LLM needs clearer instructions to answer safely and accurately.

In Day 9, the model sometimes gave imperfect answers even when the correct context was retrieved. A stronger prompt helps the model understand that it should:

- use only the provided context
- avoid outside knowledge
- avoid making up information
- answer in a clear format
- include sources
- say when the answer is not found

A better prompt improves answer quality and reduces hallucination.

---

### 2. What is hallucination in RAG?

Hallucination happens when an AI model gives an answer that is not supported by the provided documents.

Example:

If the documents do not mention maternity leave, but the model invents a maternity leave policy, that is hallucination.

In RAG, hallucination can happen when:

- retrieval returns irrelevant chunks
- the prompt is weak
- the model ignores the context
- the model uses outside knowledge
- the model guesses when information is missing

The goal of RAG is to reduce hallucination by forcing the answer to be grounded in retrieved documents.

---

### 3. Why do we use a retrieval relevance check?

We use a retrieval relevance check to decide whether the retrieved chunks are good enough to answer the question.

If the top retrieved chunk is not relevant, we should not send it to the LLM as if it contains the answer. That could cause the model to guess or generate a wrong answer.

The relevance check helps the system safely respond:

"I could not find the answer in the provided documents."

This makes the RAG system more trustworthy.

---

### 4. What does `MAX_DISTANCE_THRESHOLD` do?

`MAX_DISTANCE_THRESHOLD` is used to decide whether the top retrieved chunk is relevant enough.

In our script:

```python
MAX_DISTANCE_THRESHOLD = 1.25

If the best retrieved chunk has a distance less than or equal to 1.25, we treat it as relevant.

If the best distance is greater than 1.25, we treat retrieval as weak and return:

I could not find the answer in the provided documents.

Simple rule:

Lower distance = better match
Higher distance = weaker match

5. What does build_sources() do?

build_sources() creates a clean list of source references from the retrieved chunks.

It uses the file name and chunk number to create citations like:

remote_work_policy.txt#chunk-1
it_security_policy.txt#chunk-2

This helps show where the answer came from.

It also removes duplicate sources so the final source list is cleaner.

6. Why do we include citations/sources in the answer?

We include citations and sources so users can verify the answer.

Citations make the RAG system more trustworthy because they show the exact document and chunk used to generate the answer.

Sources are useful for:

trust
verification
debugging
compliance
explaining why the model gave a certain answer

In enterprise AI systems, source tracking is very important because users should know where the information came from.

7. What should the system do when the answer is not in the documents?

When the answer is not in the documents, the system should clearly say:

I could not find the answer in the provided documents.

It should not guess or use outside knowledge.

This is important because RAG systems should be grounded in the available documents. If the documents do not contain the answer, the safest behavior is to say that the answer was not found.

8. Why can a small local model still give imperfect answers?

A small local model like gemma3:1b can still give imperfect answers because it has limited reasoning and instruction-following ability compared to larger models.

It may sometimes:

ignore part of the prompt
misunderstand the context
say the answer is missing even when it is present
generate awkward wording
fail to follow the requested answer format
hallucinate

This does not mean the RAG pipeline is wrong. It means the generation model has limitations.

Better prompts, better retrieval, larger models, and evaluation checks can improve performance.

9. How is Day 10 more production-like than Day 9?

Day 10 is more production-like because it adds safety and reliability improvements.

Compared to Day 9, Day 10 includes:

stronger prompt instructions
citation/source formatting
retrieval relevance checking
safer handling for unknown questions
cleaner saved output
better debugging information
top distance tracking

These are important features in real AI systems because production RAG systems need to be reliable, explainable, and safe.

10. What output file was created?

The output file created was:

day10_improved_rag_results.csv

It contains:

question
answer
retrieval_relevant
top_source_file
top_chunk_id
top_distance
sources
context

This file stores the improved RAG answers, retrieval quality information, source citations, and retrieved context.