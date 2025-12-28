# Quickstart: RAG Pipeline

## Prerequisites
- Python 3.11 or higher
- UV package manager
- Access to Cohere API (API key)
- Access to Qdrant Cloud (URL and API key)
- Target Docusaurus website URL

## Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Create Backend Directory
```bash
mkdir backend
cd backend
```

### 3. Initialize Project with UV
```bash
uv init
```

### 4. Install Dependencies
```bash
uv add requests beautifulsoup4 cohere qdrant-client python-dotenv
```

### 5. Create Environment File
Create a `.env` file in the backend directory:
```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_cloud_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
BASE_URL=https://your-docusaurus-site.com
```

## Configuration

### Processing Configuration
The pipeline can be configured via environment variables in the `.env` file:

- `COHERE_API_KEY`: Your Cohere API key
- `QDRANT_URL`: Your Qdrant Cloud instance URL
- `QDRANT_API_KEY`: Your Qdrant API key
- `BASE_URL`: The root URL of the Docusaurus website to crawl
- `CHUNK_SIZE`: Maximum size of text chunks (default: 1000 characters)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 100 characters)
- `BATCH_SIZE`: Number of chunks to process in each batch (default: 10)
- `MAX_RETRIES`: Maximum number of retries for failed operations (default: 3)

## Running the Pipeline

### 1. Execute the Main Script
```bash
cd backend
python main.py
```

### 2. Pipeline Execution Steps
The pipeline will execute in the following order:
1. **Crawling**: Fetch all pages from the Docusaurus website
2. **Text Processing**: Extract and clean text content, remove HTML markup
3. **Chunking**: Split content into appropriately sized segments
4. **Embedding**: Generate vector embeddings using Cohere
5. **Storage**: Store embeddings with metadata in Qdrant Cloud
6. **Verification**: Verify vectors are queryable and correctly indexed

### 3. Incremental Updates
To run incremental updates (only process changed/new content):
```bash
python main.py --incremental
```

## Expected Output
- Processed content stored in Qdrant Cloud with metadata
- Console logs showing progress and statistics
- Error logs for any failed operations
- Success rate metrics for each pipeline stage

## Troubleshooting

### Common Issues
1. **API Key Errors**: Verify your Cohere and Qdrant API keys are correct
2. **Crawling Errors**: Check that the BASE_URL is accessible and properly formatted
3. **Memory Issues**: Reduce BATCH_SIZE if processing large sites
4. **Rate Limits**: Adjust DELAY_BETWEEN_REQUESTS if hitting rate limits

### Verification
After running the pipeline, verify:
- All documents were processed successfully
- Embeddings are stored in Qdrant Cloud
- Vectors are queryable and correctly indexed
- Metadata is preserved (URL, section, heading, chunk index)