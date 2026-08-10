import logging
import re
from pathlib import Path
from datetime import datetime
import pandas as pd


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


BASE_DIR = Path(__file__).parent
RAW_DOCS_DIR = BASE_DIR / "raw_documents"
CLEANED_DOCS_DIR = BASE_DIR / "cleaned_documents"
OUTPUT_DIR = BASE_DIR / "output"


def read_text_file(file_path):
    try:
        logging.info(f"Reading file: {file_path.name}")
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
        raise


def clean_text(text):
    logging.info("Cleaning text")

    # Remove extra spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove extra blank lines
    text = re.sub(r"\n\s*\n", "\n\n", text)

    # Strip leading/trailing spaces
    text = text.strip()

    return text


def create_metadata(file_path, raw_text, cleaned_text):
    metadata = {
        "file_name": file_path.name,
        "file_type": file_path.suffix,
        "raw_character_count": len(raw_text),
        "cleaned_character_count": len(cleaned_text),
        "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return metadata


def save_cleaned_text(file_name, cleaned_text):
    CLEANED_DOCS_DIR.mkdir(exist_ok=True)

    output_file = CLEANED_DOCS_DIR / file_name

    logging.info(f"Saving cleaned file: {output_file.name}")

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(cleaned_text)


def process_documents():
    logging.info("Starting document processing pipeline")

    OUTPUT_DIR.mkdir(exist_ok=True)

    metadata_records = []

    text_files = list(RAW_DOCS_DIR.glob("*.txt"))

    if not text_files:
        logging.warning("No text files found in raw_documents folder")
        return

    for file_path in text_files:
        raw_text = read_text_file(file_path)
        cleaned_text = clean_text(raw_text)

        metadata = create_metadata(file_path, raw_text, cleaned_text)
        metadata_records.append(metadata)

        save_cleaned_text(file_path.name, cleaned_text)

    metadata_df = pd.DataFrame(metadata_records)
    metadata_output_path = OUTPUT_DIR / "document_metadata.csv"

    logging.info("Saving document metadata")
    metadata_df.to_csv(metadata_output_path, index=False)

    logging.info("Document processing pipeline completed successfully")


if __name__ == "__main__":
    process_documents()