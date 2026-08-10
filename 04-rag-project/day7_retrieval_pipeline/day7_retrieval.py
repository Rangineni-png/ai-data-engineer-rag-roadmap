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
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return model


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
            "question": question,
            "chunk_id": ids[i],
            "file_name": metadatas[i]["file_name"],
            "chunk_number": metadatas[i]["chunk_number"],
            "distance": distances[i],
            "chunk_text": documents[i]
        })

    return retrieved_chunks


def display_retrieved_chunks(retrieved_chunks):
    print("\nRetrieved Chunks")
    print("=" * 70)

    for chunk in retrieved_chunks:
        print(f"\nRank: {chunk['rank']}")
        print(f"Chunk ID: {chunk['chunk_id']}")
        print(f"File Name: {chunk['file_name']}")
        print(f"Chunk Number: {chunk['chunk_number']}")
        print(f"Distance: {chunk['distance']:.4f}")
        print(f"Text: {chunk['chunk_text']}")


def save_retrieval_results(retrieved_chunks, file_name):
    OUTPUT_DIR.mkdir(exist_ok=True)

    output_file = OUTPUT_DIR / file_name

    results_df = pd.DataFrame(retrieved_chunks)
    results_df.to_csv(output_file, index=False)

    logging.info(f"Saved retrieval results to: {output_file}")


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
        retrieved_chunks = retrieve_chunks(
            question=question,
            model=model,
            collection=collection,
            top_k=3
        )

        display_retrieved_chunks(retrieved_chunks)

        all_results.extend(retrieved_chunks)

    save_retrieval_results(
        retrieved_chunks=all_results,
        file_name="day7_retrieval_results.csv"
    )

    logging.info("Retrieval pipeline completed successfully")


if __name__ == "__main__":
    main()