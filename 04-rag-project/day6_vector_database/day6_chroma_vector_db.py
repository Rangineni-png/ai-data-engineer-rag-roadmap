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

CHUNKS_FILE = PROJECT_DIR / "day4_chunking" / "output" / "document_chunks.csv"
CHROMA_DB_DIR = BASE_DIR / "chroma_db"
OUTPUT_DIR = BASE_DIR / "output"

COLLECTION_NAME = "company_policy_chunks"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_chunks(file_path):
    if not file_path.exists():
        raise FileNotFoundError(f"Chunks file not found: {file_path}")

    logging.info(f"Loading chunks from: {file_path}")

    chunks_df = pd.read_csv(file_path)

    required_columns = ["chunk_id", "chunk_text", "file_name", "chunk_number", "word_count"]

    for column in required_columns:
        if column not in chunks_df.columns:
            raise ValueError(f"Missing required column: {column}")

    chunks_df = chunks_df.dropna(subset=["chunk_text"])
    chunks_df = chunks_df[chunks_df["chunk_text"].str.strip() != ""]

    logging.info(f"Loaded {len(chunks_df)} chunks")

    return chunks_df


def load_embedding_model():
    logging.info(f"Loading embedding model: {EMBEDDING_MODEL_NAME}")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return model


def create_chroma_client():
    logging.info(f"Creating ChromaDB client at: {CHROMA_DB_DIR}")

    client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))

    return client


def reset_collection(client, collection_name):
    existing_collections = [collection.name for collection in client.list_collections()]

    if collection_name in existing_collections:
        logging.info(f"Deleting existing collection: {collection_name}")
        client.delete_collection(name=collection_name)

    logging.info(f"Creating collection: {collection_name}")

    collection = client.create_collection(name=collection_name)

    return collection


def prepare_chroma_records(chunks_df, model):
    logging.info("Preparing ChromaDB records")

    ids = []
    documents = []
    metadatas = []
    embeddings = []

    for _, row in chunks_df.iterrows():
        chunk_id = str(row["chunk_id"])
        chunk_text = str(row["chunk_text"])

        metadata = {
            "file_name": str(row["file_name"]),
            "chunk_number": int(row["chunk_number"]),
            "word_count": int(row["word_count"])
        }

        embedding = model.encode(
            chunk_text,
            normalize_embeddings=True
        ).tolist()

        ids.append(chunk_id)
        documents.append(chunk_text)
        metadatas.append(metadata)
        embeddings.append(embedding)

    return ids, documents, metadatas, embeddings


def add_records_to_chroma(collection, ids, documents, metadatas, embeddings):
    logging.info("Adding records to ChromaDB collection")

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings
    )

    logging.info(f"Added {len(ids)} records to ChromaDB")


def search_chroma(collection, query, model, top_k=3):
    logging.info(f"Searching ChromaDB for query: {query}")

    query_embedding = model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results


def display_results(results):
    print("\nChromaDB Search Results")
    print("=" * 60)

    ids = results["ids"][0]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    result_records = []

    for i in range(len(ids)):
        print(f"\nResult {i + 1}")
        print(f"Chunk ID: {ids[i]}")
        print(f"File Name: {metadatas[i]['file_name']}")
        print(f"Chunk Number: {metadatas[i]['chunk_number']}")
        print(f"Distance: {distances[i]:.4f}")
        print(f"Text: {documents[i]}")

        result_records.append({
            "rank": i + 1,
            "chunk_id": ids[i],
            "file_name": metadatas[i]["file_name"],
            "chunk_number": metadatas[i]["chunk_number"],
            "distance": distances[i],
            "chunk_text": documents[i]
        })

    return result_records


def save_search_results(result_records):
    OUTPUT_DIR.mkdir(exist_ok=True)

    output_file = OUTPUT_DIR / "day6_search_results.csv"

    results_df = pd.DataFrame(result_records)
    results_df.to_csv(output_file, index=False)

    logging.info(f"Saved search results to: {output_file}")


def main():
    chunks_df = load_chunks(CHUNKS_FILE)

    model = load_embedding_model()

    client = create_chroma_client()

    collection = reset_collection(client, COLLECTION_NAME)

    ids, documents, metadatas, embeddings = prepare_chroma_records(chunks_df, model)

    add_records_to_chroma(
        collection=collection,
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings
    )

    test_query = "How many days can employees work remotely?"

    results = search_chroma(
        collection=collection,
        query=test_query,
        model=model,
        top_k=3
    )

    result_records = display_results(results)

    save_search_results(result_records)

    logging.info("Vector database pipeline completed successfully")


if __name__ == "__main__":
    main()