# Lightweight RAG System (CPU-Only) for Document Q&A

This repository is a compact retrieval-augmented generation (RAG) project for asking questions about local documents using a CPU-only stack. It is designed for document understanding workflows where you want to ingest files, build a vector search index, retrieve relevant passages, and generate answers without depending on a GPU.

The project is intentionally lightweight and easy to extend: it loads common document formats, embeds the text with a sentence-transformer model, stores the embeddings in a local vector database, and uses an LLM to summarize the most relevant matches.

## What this project does

At a high level, the system does the following:

1. Loads documents from a local `data/` folder.
2. Supports common file formats including PDF, TXT, CSV, Excel, DOCX, and JSON.
3. For PDF documents, it attempts to combine normal extracted text with OCR text from images.
4. Creates embeddings using a sentence-transformer model (`all-MiniLM-L6-v2`).
5. Stores the embeddings in a Chroma vector database on disk.
6. Searches for the most relevant chunks for a user query.
7. Sends the retrieved passages to a Groq-hosted LLM for a final answer summary.

This makes it useful for small-scale document Q&A systems such as internal knowledge bases, PDF manuals, scanned reports, and other text-heavy repositories.

## Core workflow

The repository follows a standard RAG pattern:

- `src/data_loader.py`: Reads supported document types and converts them to LangChain `Document` objects.
- `src/ocr_loader.py`: Extracts OCR text from PDF pages.
- `src/embedding.py`: Splits documents into chunks and creates embeddings.
- `src/vectorstore.py`: Builds and loads a Chroma vector database.
- `src/search.py`: Queries the vector store and invokes an LLM to summarize results.
- `app.py`: Example application entry point that builds a local index and runs a sample query.

## Repository structure

```text
.
├── app.py
├── main.py
├── README.md
├── pyproject.toml
├── requirements.txt
├── notebook/
│   ├── document.ipynb
│   └── pdf_loader.ipynb
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── embedding.py
│   ├── ocr_loader.py
│   ├── search.py
│   ├── vectorstore.py
│   └── cpoldVector.txt
└── uv.lock
```

## Supported document types

The loader is built to handle:

- PDF
- TXT
- CSV
- Excel (.xlsx)
- DOCX
- JSON

For PDFs, the project combines:

- standard PDF text extraction via PyMuPDF/PyPDF
- OCR for image-based pages via Tesseract

## Tech stack

This project uses:

- Python
- LangChain + LangChain Community
- Chroma for vector storage
- Sentence Transformers for embeddings
- Hugging Face embedding model (`all-MiniLM-L6-v2`)
- Groq LLM inference
- PyMuPDF, PyPDF, OCR support, and local document loaders

## Quick start

### 1) Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate  # Windows
```

### 2) Install dependencies

Using pip:

```bash
pip install -r requirements.txt
```

Or with the project config:

```bash
pip install -e .
```

### 3) Prepare your documents

Place your files in a folder named `data/` in the project root:

```text
project-root/
├── data/
│   ├── manual.pdf
│   ├── notes.txt
│   └── report.xlsx
└── ...
```

### 4) Configure the LLM

This project uses Groq in `src/search.py`. You should provide your API key in a `.env` file or edit the code to set it appropriately.

Example:

```bash
GROQ_API_KEY=your_api_key_here
```

### 5) Run the sample app

```bash
python app.py
```

This loads the documents, builds a local Chroma vector store, and executes a sample query.

## Notes on environment setup

A few practical requirements should be considered:

- Tesseract must be installed on the machine and accessible on `PATH`.
- On Windows, the OCR path is currently configured in `src/ocr_loader.py` to a hardcoded install location:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

If your installation is elsewhere, update that path to match your system.

- The code is suitable for local experimentation and small document corpora; it is not optimized for large-scale enterprise ingestion out of the box.

## Example usage

The project is meant to answer questions like:

- "How do I connect the input card?"
- "What does this policy say about data retention?"
- "Summarize the key steps described in this PDF."

The query is matched against the vectorized document chunks, and the LLM summarizes the retrieved context.

## Important implementation details

This repository is a simple educational/demo implementation rather than a production-ready platform. Some parts are intentionally minimal and can be improved for real-world use:

- hardcoded sample queries
- local-only storage and indexing
- direct Groq configuration in code
- basic document ingestion without more advanced chunking or metadata filtering

## Why this repo is useful

It demonstrates a full local-document RAG workflow in a compact codebase, which makes it helpful for:

- learning how retrieval and summarization work together
- prototyping document Q&A on CPU-only hardware
- testing PDF + OCR ingestion and embeddings before scaling up

## Future improvements

Potential enhancements include:

- configurable model and folder paths
- better chunking and metadata handling
- support for a richer UI or API layer
- persistent retrieval with indexing improvements
- model selection via environment variables
- robust error handling and logging

## Summary

This repository implements a lightweight CPU-only RAG system for document question answering. It reads local documents, creates embeddings, stores them in a vector database, retrieves relevant passages, and uses an LLM to answer questions grounded in the document content.

It is a good starter project for anyone wanting to build a small, local, document-based AI assistant without GPU requirements.
