import logging
from pathlib import Path
import requests
import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


BASE_DIR = Path(__file__).parent
PROJECT_DIR = BASE_DIR.parent

CHROMA_DB_DIR = PROJECT_DIR / "day6_vector_database" / "chroma_db"
OUTPUT_DIR = BASE_DIR / "output"

COLLECTION_NAME = "company_policy_chunks"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "gemma3:1b"


def load_embedding_model():
    logging.info(f"Loading embedding model: {EMBEDDING_MODEL_NAME}")
    return SentenceTransformer(EMBEDDING_MODEL_NAME)


def connect_to_chroma():
    logging.info(f"Connecting to ChromaDB at: {CHROMA_DB_DIR}")

    if not CHROMA_DB_DIR.exists():
        raise FileNotFoundError(
            f"ChromaDB folder not found: {CHROMA_DB_DIR}. Run Day 6 first."
        )

    client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))
    collection = client.get_collection(name=COLLECTION_NAME)

    logging.info(f"Connected to collection: {COLLECTION_NAME}")
    return collection


def retrieve_chunks(question, model, collection, top_k=3):
    logging.info(f"Retrieving chunks for question: {question}")

    question_embedding = model.encode(
        question,
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k
    )

    retrieved_chunks = []

    ids = results["ids"][0]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for i in range(len(ids)):
        retrieved_chunks.append({
            "rank": i + 1,
            "chunk_id": ids[i],
            "file_name": metadatas[i]["file_name"],
            "chunk_number": metadatas[i]["chunk_number"],
            "distance": distances[i],
            "chunk_text": documents[i]
        })

    return retrieved_chunks


def build_context(retrieved_chunks):
    context_parts = []

    for chunk in retrieved_chunks:
        context_part = (
            f"[Source: {chunk['file_name']}, Chunk: {chunk['chunk_number']}]\n"
            f"{chunk['chunk_text']}"
        )
        context_parts.append(context_part)

    return "\n\n---\n\n".join(context_parts)


def build_prompt(question, context):
    prompt = f"""
You are answering questions using company policy documents.

Use ONLY the context below.
The context contains the answer if it is relevant.

Instructions:
- Give a direct answer in 1-2 sentences.
- Do not say the answer is missing if the context contains relevant information.
- Include the source file name and chunk number.
- If the context truly does not contain the answer, say:
  "I could not find the answer in the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""
    return prompt


def call_ollama(prompt):
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip()

    except requests.exceptions.ConnectionError:
        raise ConnectionError(
            "Could not connect to Ollama. Make sure Ollama is installed and running."
        )
    except requests.exceptions.Timeout:
        raise TimeoutError("Ollama request timed out.")
    except Exception as e:
        raise RuntimeError(f"Error calling Ollama: {e}")


def process_question(question, model, collection, top_k=3):
    retrieved_chunks = retrieve_chunks(
        question=question,
        model=model,
        collection=collection,
        top_k=top_k
    )

    context = build_context(retrieved_chunks)
    prompt = build_prompt(question, context)
    answer = call_ollama(prompt)

    result = {
        "question": question,
        "answer": answer,
        "top_source_file": retrieved_chunks[0]["file_name"],
        "top_chunk_id": retrieved_chunks[0]["chunk_id"],
        "top_distance": retrieved_chunks[0]["distance"],
        "context": context
    }

    return result


def display_answer(result):
    print("\nQuestion")
    print("=" * 70)
    print(result["question"])

    print("\nOllama RAG Answer")
    print("=" * 70)
    print(result["answer"])

    print("\nTop Retrieved Source")
    print("=" * 70)
    print(f"{result['top_source_file']} | {result['top_chunk_id']}")
    print(f"Distance: {result['top_distance']:.4f}")


def save_results(results):
    OUTPUT_DIR.mkdir(exist_ok=True)

    output_file = OUTPUT_DIR / "day9_ollama_rag_answers.csv"

    results_df = pd.DataFrame(results)
    results_df.to_csv(output_file, index=False)

    logging.info(f"Saved Ollama RAG answers to: {output_file}")


def main():
    model = load_embedding_model()
    collection = connect_to_chroma()

    questions = [
        "How many days can employees work remotely?",
        "Can employees share passwords?",
        "How many vacation days do full-time employees receive?",
        "Where should suspicious emails be reported?",
        "What is my name?"
    ]

    all_results = []

    for question in questions:
        result = process_question(
            question=question,
            model=model,
            collection=collection,
            top_k=3
        )

        display_answer(result)
        all_results.append(result)

    save_results(all_results)

    logging.info("Ollama RAG pipeline completed successfully")


if __name__ == "__main__":
    main()