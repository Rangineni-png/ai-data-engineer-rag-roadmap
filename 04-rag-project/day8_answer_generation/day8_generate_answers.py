import logging
from pathlib import Path
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
            f"Source: {chunk['file_name']}, Chunk: {chunk['chunk_number']}\n"
            f"Text: {chunk['chunk_text']}"
        )
        context_parts.append(context_part)

    context = "\n\n---\n\n".join(context_parts)

    return context


def generate_simple_answer(question, retrieved_chunks):
    """
    This is a simple rule-based answer generator for Day 8.
    Later, we will replace this with an LLM/Ollama.
    """

    best_chunk = retrieved_chunks[0]
    best_text = best_chunk["chunk_text"]
    source = best_chunk["file_name"]
    chunk_number = best_chunk["chunk_number"]

    answer = (
        f"Based on the retrieved company policy context, the answer is:\n\n"
        f"{best_text}\n\n"
        f"Source: {source}, chunk {chunk_number}"
    )

    return answer


def process_question(question, model, collection, top_k=3):
    retrieved_chunks = retrieve_chunks(
        question=question,
        model=model,
        collection=collection,
        top_k=top_k
    )

    context = build_context(retrieved_chunks)
    answer = generate_simple_answer(question, retrieved_chunks)

    result = {
        "question": question,
        "answer": answer,
        "context": context,
        "top_source_file": retrieved_chunks[0]["file_name"],
        "top_chunk_id": retrieved_chunks[0]["chunk_id"],
        "top_distance": retrieved_chunks[0]["distance"]
    }

    return result


def display_answer(result):
    print("\nQuestion")
    print("=" * 70)
    print(result["question"])

    print("\nGenerated Answer")
    print("=" * 70)
    print(result["answer"])

    print("\nTop Source")
    print("=" * 70)
    print(f"{result['top_source_file']} | {result['top_chunk_id']}")
    print(f"Distance: {result['top_distance']:.4f}")


def save_answers(results):
    OUTPUT_DIR.mkdir(exist_ok=True)

    output_file = OUTPUT_DIR / "day8_generated_answers.csv"

    results_df = pd.DataFrame(results)
    results_df.to_csv(output_file, index=False)

    logging.info(f"Saved generated answers to: {output_file}")


def main():
    model = load_embedding_model()
    collection = connect_to_chroma()

    questions = [
        "How many days can employees work remotely?",
        "Can employees share passwords?",
        "How many vacation days do full-time employees receive?",
        "Where should suspicious emails be reported?"
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

    save_answers(all_results)

    logging.info("Answer generation pipeline completed successfully")


if __name__ == "__main__":
    main()