# RAG Pipeline Backend

This project implements a RAG (Retrieval-Augmented Generation) pipeline that:

1. Crawls Docusaurus documentation websites
2. Extracts and processes text content
3. Generates vector embeddings using Cohere
4. Stores embeddings with metadata in Qdrant Cloud

## Setup

1. Install dependencies: `uv sync`
2. Copy `.env.example` to `.env` and add your API keys:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` to add your actual API keys and URLs
4. Run the pipeline: `python main.py`

## Configuration

The pipeline can be configured via environment variables in `.env`:

- `COHERE_API_KEY`: Your Cohere API key
- `QDRANT_URL`: Your Qdrant Cloud instance URL
- `QDRANT_API_KEY`: Your Qdrant API key
- `BASE_URL`: The root URL of the Docusaurus website to crawl
- `CHUNK_SIZE`: Maximum size of text chunks (default: 1000 characters)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 100 characters)
- `BATCH_SIZE`: Number of chunks to process in each batch (default: 10)
- `MAX_RETRIES`: Maximum number of retries for failed operations (default: 3)
- `DELAY_BETWEEN_REQUESTS`: Delay in seconds between HTTP requests (default: 1.0)

## Usage

Run the pipeline with default configuration:
```bash
python main.py
```

Run the pipeline with custom configuration via command line arguments:
```bash
python main.py --base-url "https://your-docusaurus-site.com" --chunk-size 2000
```

## Security Notice

⚠️ **IMPORTANT**: Never commit your `.env` file to version control. The `.env` file contains sensitive API keys and should be kept private. The `.env.example` file contains placeholder values for reference only.

## Command Line Options

The pipeline supports the following command line arguments:
- `--base-url`: Base URL of the Docusaurus website to crawl
- `--chunk-size`: Maximum size of text chunks
- `--chunk-overlap`: Overlap between text chunks
- `--batch-size`: Number of chunks to process in each batch
- `--max-retries`: Maximum number of retries for failed operations
- `--delay-between-requests`: Delay in seconds between HTTP requests