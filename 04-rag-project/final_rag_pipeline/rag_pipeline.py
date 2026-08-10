import logging
import re
from pathlib import Path
from datetime import datetime

import requests
import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).parent

LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOGS_DIR / "rag_pipeline.log"),
        logging.StreamHandler()
    ]
)


RAW_DOCS_DIR = BASE_DIR / "data" / "raw_documents"
CLEANED_DOCS_DIR = BASE_DIR / "data" / "cleaned_documents"
OUTPUT_DIR = BASE_DIR / "data" / "output"
CHROMA_DB_DIR = BASE_DIR / "vector_db"

COLLECTION_NAME = "company_policy_chunks"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "gemma3:1b"

CHUNK_SIZE = 40
CHUNK_OVERLAP = 10
TOP_K = 3
MAX_DISTANCE_THRESHOLD = 1.25


def clean_text(text):
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n", "\n\n", text)
    return text.strip()


def load_raw_documents():
    logging.info("Loading raw documents")

    documents = []

    text_files = list(RAW_DOCS_DIR.glob("*.txt"))

    if not text_files:
        raise FileNotFoundError(f"No text files found in {RAW_DOCS_DIR}")

    for file_path in text_files:
        with open(file_path, "r", encoding="utf-8") as file:
            raw_text = file.read()

        cleaned_text = clean_text(raw_text)

        documents.append({
            "file_name": file_path.name,
            "file_type": file_path.suffix,
            "raw_text": raw_text,
            "cleaned_text": cleaned_text,
            "raw_character_count": len(raw_text),
            "cleaned_character_count": len(cleaned_text),
            "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    logging.info(f"Loaded {len(documents)} documents")
    return documents


def validate_documents(documents):
    logging.info("Running document data quality checks")

    if not documents:
        raise ValueError("No documents were loaded.")

    valid_documents = []

    for doc in documents:
        file_name = doc["file_name"]
        cleaned_text = doc["cleaned_text"]

        if not cleaned_text:
            logging.warning(f"Skipping empty document: {file_name}")
            continue

        if len(cleaned_text.split()) < 5:
            logging.warning(f"Skipping document with too few words: {file_name}")
            continue

        valid_documents.append(doc)

    if not valid_documents:
        raise ValueError("No valid documents available after data quality checks.")

    logging.info(f"{len(valid_documents)} documents passed data quality checks")
    return valid_documents


def save_cleaned_documents(documents):
    logging.info("Saving cleaned documents")
    CLEANED_DOCS_DIR.mkdir(parents=True, exist_ok=True)

    metadata_records = []

    for doc in documents:
        output_file = CLEANED_DOCS_DIR / doc["file_name"]

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(doc["cleaned_text"])

        metadata_records.append({
            "file_name": doc["file_name"],
            "file_type": doc["file_type"],
            "raw_character_count": doc["raw_character_count"],
            "cleaned_character_count": doc["cleaned_character_count"],
            "processed_at": doc["processed_at"]
        })

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    metadata_df = pd.DataFrame(metadata_records)
    metadata_df.to_csv(OUTPUT_DIR / "document_metadata.csv", index=False)


def chunk_text_by_words(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    words = text.split()

    chunks = []
    start = 0
    chunk_number = 1

    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]

        chunk_text = " ".join(chunk_words)

        chunks.append({
            "chunk_number": chunk_number,
            "chunk_text": chunk_text,
            "word_count": len(chunk_words)
        })

        chunk_number += 1
        start += chunk_size - overlap

    return chunks


def create_document_chunks(documents):
    logging.info("Creating document chunks")

    chunk_records = []

    for doc in documents:
        chunks = chunk_text_by_words(doc["cleaned_text"])

        file_stem = Path(doc["file_name"]).stem

        for chunk in chunks:
            chunk_id = f"{file_stem}_chunk_{chunk['chunk_number']}"

            chunk_records.append({
                "chunk_id": chunk_id,
                "file_name": doc["file_name"],
                "source_type": doc["file_type"],
                "chunk_number": chunk["chunk_number"],
                "chunk_text": chunk["chunk_text"],
                "word_count": chunk["word_count"],
                "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

    chunks_df = pd.DataFrame(chunk_records)
    chunks_df.to_csv(OUTPUT_DIR / "document_chunks.csv", index=False)

    logging.info(f"Created {len(chunks_df)} chunks")
    return chunks_df


def load_embedding_model():
    logging.info(f"Loading embedding model: {EMBEDDING_MODEL_NAME}")
    return SentenceTransformer(EMBEDDING_MODEL_NAME)


def create_chroma_collection():
    logging.info("Creating ChromaDB collection")

    client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))

    existing_collections = [collection.name for collection in client.list_collections()]

    if COLLECTION_NAME in existing_collections:
        logging.info(f"Deleting existing collection: {COLLECTION_NAME}")
        client.delete_collection(name=COLLECTION_NAME)

    collection = client.create_collection(name=COLLECTION_NAME)

    return collection


def add_chunks_to_chroma(chunks_df, model, collection):
    logging.info("Adding chunks to ChromaDB")

    ids = []
    documents = []
    metadatas = []
    embeddings = []

    for _, row in chunks_df.iterrows():
        chunk_text = str(row["chunk_text"])

        embedding = model.encode(
            chunk_text,
            normalize_embeddings=True
        ).tolist()

        ids.append(str(row["chunk_id"]))
        documents.append(chunk_text)
        metadatas.append({
            "file_name": str(row["file_name"]),
            "chunk_number": int(row["chunk_number"]),
            "word_count": int(row["word_count"])
        })
        embeddings.append(embedding)

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings
    )

    logging.info(f"Added {len(ids)} chunks to ChromaDB")


def build_knowledge_base():
    logging.info("Building knowledge base")

    documents = load_raw_documents()
    documents = validate_documents(documents)
    save_cleaned_documents(documents)

    chunks_df = create_document_chunks(documents)

    model = load_embedding_model()
    collection = create_chroma_collection()

    add_chunks_to_chroma(chunks_df, model, collection)

    logging.info("Knowledge base built successfully")

    return model, collection


def connect_to_existing_collection():
    logging.info("Connecting to existing ChromaDB collection")

    model = load_embedding_model()

    client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))
    collection = client.get_collection(name=COLLECTION_NAME)

    return model, collection


def retrieve_chunks(question, model, collection, top_k=TOP_K):
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
        sources.append(f"{chunk['file_name']}#chunk-{chunk['chunk_number']}")

    return "; ".join(list(dict.fromkeys(sources)))


def build_prompt(question, context):
    return f"""
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
        answer = data.get("response", "").strip()

        if not answer:
            raise ValueError("Ollama returned an empty response.")

        return answer

    except requests.exceptions.ConnectionError:
        logging.error("Could not connect to Ollama. Make sure Ollama is running.")
        return (
            "Answer: The local LLM service is not available. "
            "Please make sure Ollama is running.\n"
            "Sources: None"
        )

    except requests.exceptions.Timeout:
        logging.error("Ollama request timed out.")
        return (
            "Answer: The local LLM request timed out. Please try again.\n"
            "Sources: None"
        )

    except Exception as e:
        logging.error(f"Ollama error: {e}")
        return (
            "Answer: An error occurred while generating the answer.\n"
            "Sources: None"
        )


def validate_question(question):
    if question is None:
        raise ValueError("Question cannot be None.")

    question = question.strip()

    if not question:
        raise ValueError("Question cannot be empty.")

    if len(question) < 3:
        raise ValueError("Question is too short.")

    if len(question) > 500:
        raise ValueError("Question is too long. Please keep it under 500 characters.")

    return question


def answer_question(question, model, collection):
    question = validate_question(question)

    logging.info(f"Answering question: {question}")

    retrieved_chunks = retrieve_chunks(question, model, collection)

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

        if "could not find" in answer.lower():
            top_chunk = retrieved_chunks[0]
            answer = (
                f"Answer: {top_chunk['chunk_text']}\n"
                f"Sources: {top_chunk['file_name']}#chunk-{top_chunk['chunk_number']}"
            )

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


def save_results(results):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    results_df = pd.DataFrame(results)
    results_df.to_csv(OUTPUT_DIR / "final_rag_results.csv", index=False)

    logging.info(f"Saved results to {OUTPUT_DIR / 'final_rag_results.csv'}")


def main():
    model, collection = build_knowledge_base()

    questions = [
        "How many days can employees work remotely?",
        "Can employees share passwords?",
        "How many vacation days do full-time employees receive?",
        "Where should suspicious emails be reported?",
        "What is my name?"
    ]

    results = []

    for question in questions:
        result = answer_question(question, model, collection)

        print("\nQuestion")
        print("=" * 70)
        print(result["question"])

        print("\nAnswer")
        print("=" * 70)
        print(result["answer"])

        print("\nTop Source")
        print("=" * 70)
        print(result["top_source_file"], result["top_chunk_id"])
        print(f"Distance: {result['top_distance']}")

        results.append(result)

    save_results(results)

    logging.info("Final RAG pipeline completed successfully")


if __name__ == "__main__":
    main()

