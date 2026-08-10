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

TOP_K = 3
MAX_DISTANCE_THRESHOLD = 1.25


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


def retrieve_chunks(question, model, collection, top_k=TOP_K):
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


def is_retrieval_relevant(retrieved_chunks):
    if not retrieved_chunks:
        return False

    best_distance = retrieved_chunks[0]["distance"]

    return best_distance <= MAX_DISTANCE_THRESHOLD


def build_context(retrieved_chunks):
    context_parts = []

    for chunk in retrieved_chunks:
        context_part = (
            f"[{chunk['rank']}] "
            f"Source: {chunk['file_name']} | "
            f"Chunk: {chunk['chunk_number']} | "
            f"Distance: {chunk['distance']:.4f}\n"
            f"{chunk['chunk_text']}"
        )
        context_parts.append(context_part)

    return "\n\n---\n\n".join(context_parts)


def build_sources(retrieved_chunks):
    sources = []

    for chunk in retrieved_chunks:
        source = f"{chunk['file_name']}#chunk-{chunk['chunk_number']}"
        sources.append(source)

    unique_sources = list(dict.fromkeys(sources))

    return "; ".join(unique_sources)


def build_prompt(question, context):
    prompt = f"""
You are a careful AI assistant answering company policy questions.

Use ONLY the provided context.
Do not use outside knowledge.
Do not invent details.
If the answer is not clearly supported by the context, say:
"I could not find the answer in the provided documents."

Answer format:
Answer: <direct answer in 1-3 sentences>
Sources: <file name and chunk number>

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


def generate_answer(question, model, collection):
    retrieved_chunks = retrieve_chunks(
        question=question,
        model=model,
        collection=collection,
        top_k=TOP_K
    )

    retrieval_relevant = is_retrieval_relevant(retrieved_chunks)
    context = build_context(retrieved_chunks)
    sources = build_sources(retrieved_chunks)

    if not retrieval_relevant:
        answer = (
            "Answer: I could not find the answer in the provided documents.\n"
            "Sources: None"
        )
    else:
        prompt = build_prompt(question, context)
        answer = call_ollama(prompt)

    result = {
        "question": question,
        "answer": answer,
        "retrieval_relevant": retrieval_relevant,
        "top_source_file": retrieved_chunks[0]["file_name"] if retrieved_chunks else None,
        "top_chunk_id": retrieved_chunks[0]["chunk_id"] if retrieved_chunks else None,
        "top_distance": retrieved_chunks[0]["distance"] if retrieved_chunks else None,
        "sources": sources if retrieval_relevant else "None",
        "context": context
    }

    return result


def display_result(result):
    print("\nQuestion")
    print("=" * 70)
    print(result["question"])

    print("\nAnswer")
    print("=" * 70)
    print(result["answer"])

    print("\nRetrieval Info")
    print("=" * 70)
    print(f"Relevant retrieval: {result['retrieval_relevant']}")
    print(f"Top source: {result['top_source_file']}")
    print(f"Top chunk: {result['top_chunk_id']}")
    print(f"Top distance: {result['top_distance']}")
    print(f"Sources: {result['sources']}")


def save_results(results):
    OUTPUT_DIR.mkdir(exist_ok=True)

    output_file = OUTPUT_DIR / "day10_improved_rag_results.csv"

    results_df = pd.DataFrame(results)
    results_df.to_csv(output_file, index=False)

    logging.info(f"Saved improved RAG results to: {output_file}")


def main():
    model = load_embedding_model()
    collection = connect_to_chroma()

    questions = [
        "How many days can employees work remotely?",
        "Can employees share passwords?",
        "How many vacation days do full-time employees receive?",
        "Where should suspicious emails be reported?",
        "What is my name?",
        "What is the company's maternity leave policy?"
    ]

    results = []

    for question in questions:
        result = generate_answer(
            question=question,
            model=model,
            collection=collection
        )
        display_result(result)
        results.append(result)

    save_results(results)

    logging.info("Improved RAG pipeline completed successfully")


if __name__ == "__main__":
    main()