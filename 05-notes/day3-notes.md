# Day 3 - Document Processing for RAG

## Today’s Goal
Process raw text documents and prepare them for future RAG pipelines.

## Questions

### 1. What is a raw document?

A raw document is the original unprocessed file that contains information. It can be a text file, PDF, Word document, webpage, email, CSV file, or any other source of data.

In this task, the raw documents were:

* company_policy.txt
* it_security_policy.txt
* remote_work_policy.txt

These files are called raw documents because they are the starting input before cleaning, chunking, embeddings, and vector database storage.

---

### 2. Why do we need text extraction?

We need text extraction because AI systems cannot directly understand files like PDFs, Word documents, or webpages unless the useful text is pulled out first.

Text extraction converts document content into plain readable text that can be processed by the pipeline.

Example:

PDF or text file
→ extract readable text
→ clean text
→ chunk text
→ create embeddings

Without text extraction, we cannot prepare documents for RAG.

---

### 3. Why do we need text cleaning before chunking?

We need text cleaning before chunking because messy text creates poor-quality chunks.

If the text has extra spaces, broken lines, duplicate blank lines, page numbers, headers, or unwanted characters, the chunks may become confusing or meaningless.

Clean text helps produce better chunks, and better chunks lead to better retrieval results in RAG.

Simple rule:

Bad text → bad chunks → bad retrieval → bad AI answer

Clean text → good chunks → better retrieval → better AI answer

---

### 4. What did `clean_text()` do?

`clean_text()` cleaned the extracted text by removing extra spaces, reducing extra blank lines, and removing leading or trailing spaces.

In this task, it helped make the document text cleaner and more consistent before saving it into the `cleaned_documents` folder.

---

### 5. What metadata did we create?

The pipeline created metadata for each processed document.

The metadata included:

* file_name
* file_type
* raw_character_count
* cleaned_character_count
* processed_at

This metadata was saved into:

document_metadata.csv

---

### 6. Why is metadata important in RAG?

Metadata is important in RAG because it helps track where each piece of information came from.

For example, metadata can tell us:

* which document the text came from
* what file type it was
* when it was processed
* which page or section it came from
* which chunk ID it belongs to

Later, when the LLM gives an answer, metadata helps provide citations and source references.

Without metadata, the AI may give an answer, but users may not know where the answer came from.

---

### 7. What output files were created?

The pipeline created cleaned versions of the raw text documents inside the `cleaned_documents` folder.

The cleaned files were:

* company_policy.txt
* it_security_policy.txt
* remote_work_policy.txt

The pipeline also created a metadata file inside the `output` folder:

* document_metadata.csv

---

### 8. How is this different from the Day 2 CSV pipeline?

Day 2 focused on structured data. The input was CSV files with rows and columns, such as customers and orders.

Day 3 focused on unstructured text data. The input was policy documents written as plain text.

Day 2 pipeline:

CSV files
→ clean rows
→ validate customer IDs
→ summarize data
→ save CSV outputs

Day 3 pipeline:

Text documents
→ read text
→ clean text
→ create metadata
→ save cleaned documents

The main difference is that Day 2 worked with tabular data, while Day 3 worked with document text for future RAG processing.

---

### 9. How will this connect to embeddings and vector databases later?

The cleaned documents created in Day 3 will become the input for the next stages of the RAG pipeline.

Next, we will split the cleaned text into chunks. Then we will convert each chunk into embeddings. After that, we will store those embeddings in a vector database.

Full connection:

Raw documents
→ cleaned documents
→ chunks
→ embeddings
→ vector database
→ semantic search
→ retrieved context
→ LLM answer with citations

Day 3 completed the document cleaning and metadata preparation stage.
