import logging
from pathlib import Path
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


BASE_DIR = Path(__file__).parent
PROJECT_DIR = BASE_DIR.parent

CHUNKS_FILE = PROJECT_DIR / "day4_chunking" / "output" / "document_chunks.csv"
OUTPUT_DIR = BASE_DIR / "output"

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_chunks(file_path):
    if not file_path.exists():
        raise FileNotFoundError(f"Chunks file not found: {file_path}")

    logging.info(f"Loading chunks from: {file_path}")
    chunks_df = pd.read_csv(file_path)

    if "chunk_text" not in chunks_df.columns:
        raise ValueError("chunk_text column is missing from document_chunks.csv")

    chunks_df = chunks_df.dropna(subset=["chunk_text"])
    chunks_df = chunks_df[chunks_df["chunk_text"].str.strip() != ""]

    logging.info(f"Loaded {len(chunks_df)} chunks")

    return chunks_df


def load_embedding_model():
    logging.info(f"Loading embedding model: {EMBEDDING_MODEL_NAME}")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return model


def create_embeddings(model, texts):
    logging.info("Creating embeddings")

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    logging.info(f"Created embeddings with shape: {embeddings.shape}")

    return embeddings


def save_outputs(chunks_df, embeddings):
    OUTPUT_DIR.mkdir(exist_ok=True)

    embeddings_file = OUTPUT_DIR / "chunk_embeddings.npy"
    metadata_file = OUTPUT_DIR / "chunk_metadata.csv"

    np.save(embeddings_file, embeddings)

    metadata_df = chunks_df.copy()
    metadata_df["embedding_model"] = EMBEDDING_MODEL_NAME
    metadata_df["embedding_dimension"] = embeddings.shape[1]

    metadata_df.to_csv(metadata_file, index=False)

    logging.info(f"Saved embeddings to: {embeddings_file}")
    logging.info(f"Saved metadata to: {metadata_file}")


def semantic_search(query, model, chunks_df, embeddings, top_k=3):
    logging.info(f"Running semantic search for query: {query}")

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )[0]

    scores = np.dot(embeddings, query_embedding)

    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []

    for index in top_indices:
        result = {
            "score": scores[index],
            "chunk_id": chunks_df.iloc[index]["chunk_id"],
            "file_name": chunks_df.iloc[index]["file_name"],
            "chunk_text": chunks_df.iloc[index]["chunk_text"]
        }

        results.append(result)

    return results


def main():
    chunks_df = load_chunks(CHUNKS_FILE)

    model = load_embedding_model()

    texts = chunks_df["chunk_text"].tolist()

    embeddings = create_embeddings(model, texts)

    save_outputs(chunks_df, embeddings)

    test_query = "How many days can employees work remotely?"

    results = semantic_search(
        query=test_query,
        model=model,
        chunks_df=chunks_df,
        embeddings=embeddings,
        top_k=3
    )

    print("\nSemantic Search Results")
    print("=" * 50)

    for i, result in enumerate(results, start=1):
        print(f"\nResult {i}")
        print(f"Score: {result['score']:.4f}")
        print(f"Chunk ID: {result['chunk_id']}")
        print(f"File Name: {result['file_name']}")
        print(f"Chunk Text: {result['chunk_text']}")


if __name__ == "__main__":
    main()