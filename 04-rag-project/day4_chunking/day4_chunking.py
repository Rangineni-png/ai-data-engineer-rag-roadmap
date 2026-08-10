import logging
from pathlib import Path
from datetime import datetime
import pandas as pd


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


BASE_DIR = Path(__file__).parent
PROJECT_DIR = BASE_DIR.parent

CLEANED_DOCS_DIR = PROJECT_DIR / "day3_document_processing" / "cleaned_documents"
OUTPUT_DIR = BASE_DIR / "output"

CHUNK_SIZE = 40
CHUNK_OVERLAP = 10


def read_cleaned_document(file_path):
    try:
        logging.info(f"Reading cleaned document: {file_path.name}")
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
        raise


def chunk_text_by_words(text, chunk_size=40, overlap=10):
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


def create_chunks_for_document(file_path):
    text = read_cleaned_document(file_path)

    chunks = chunk_text_by_words(
        text,
        chunk_size=CHUNK_SIZE,
        overlap=CHUNK_OVERLAP
    )

    chunk_records = []

    for chunk in chunks:
        chunk_id = f"{file_path.stem}_chunk_{chunk['chunk_number']}"

        record = {
            "chunk_id": chunk_id,
            "file_name": file_path.name,
            "source_type": file_path.suffix,
            "chunk_number": chunk["chunk_number"],
            "chunk_text": chunk["chunk_text"],
            "word_count": chunk["word_count"],
            "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        chunk_records.append(record)

    return chunk_records


def process_all_documents():
    logging.info("Starting chunking pipeline")

    OUTPUT_DIR.mkdir(exist_ok=True)

    text_files = list(CLEANED_DOCS_DIR.glob("*.txt"))

    if not text_files:
        logging.warning("No cleaned text files found")
        return

    all_chunks = []

    for file_path in text_files:
        document_chunks = create_chunks_for_document(file_path)
        all_chunks.extend(document_chunks)

    chunks_df = pd.DataFrame(all_chunks)

    output_file = OUTPUT_DIR / "document_chunks.csv"
    chunks_df.to_csv(output_file, index=False)

    logging.info(f"Saved chunks to: {output_file}")
    logging.info(f"Total chunks created: {len(chunks_df)}")
    logging.info("Chunking pipeline completed successfully")


if __name__ == "__main__":
    process_all_documents()