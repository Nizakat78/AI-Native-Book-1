"""Main entry point for the RAG pipeline."""

import logging
import sys
import argparse
from typing import List, Dict, Any
from src.rag_pipeline.config import Config
from src.rag_pipeline.crawler import Crawler
from src.rag_pipeline.text_processor import TextProcessor, TextChunk
from src.rag_pipeline.embedder import Embedder
from src.rag_pipeline.vector_store import VectorStore


def setup_logging():
    """Set up basic logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='RAG Pipeline for content extraction and embedding')
    parser.add_argument('--base-url', type=str, help='Base URL of the Docusaurus website to crawl')
    parser.add_argument('--chunk-size', type=int, help='Maximum size of text chunks')
    parser.add_argument('--chunk-overlap', type=int, help='Overlap between text chunks')
    parser.add_argument('--batch-size', type=int, help='Number of chunks to process in each batch')
    parser.add_argument('--max-retries', type=int, help='Maximum number of retries for failed operations')
    parser.add_argument('--delay-between-requests', type=float, help='Delay in seconds between HTTP requests')

    return parser.parse_args()


def main():
    """Main function to orchestrate the RAG pipeline."""
    setup_logging()
    logger = logging.getLogger(__name__)

    # Parse command line arguments
    args = parse_arguments()

    logger.info("Starting RAG Pipeline")

    # Load configuration
    config = Config.from_env()

    # Override with command line arguments if provided
    if args.base_url:
        config.base_url = args.base_url
    if args.chunk_size:
        config.chunk_size = args.chunk_size
    if args.chunk_overlap:
        config.chunk_overlap = args.chunk_overlap
    if args.batch_size:
        config.batch_size = args.batch_size
    if args.max_retries:
        config.max_retries = args.max_retries
    if args.delay_between_requests:
        config.delay_between_requests = args.delay_between_requests

    if not config.validate():
        logger.error("Configuration validation failed. Please check your environment variables.")
        sys.exit(1)

    logger.info(f"Configuration loaded. Processing website: {config.base_url}")

    try:
        # Initialize components
        crawler = Crawler(config.base_url, config.delay_between_requests, config.max_retries)
        text_processor = TextProcessor(config.chunk_size, config.chunk_overlap)
        embedder = Embedder(config.cohere_api_key, max_retries=config.max_retries)
        vector_store = VectorStore(config.qdrant_url, config.qdrant_api_key)

        # Create collection in Qdrant
        logger.info("Creating/updating Qdrant collection...")
        if not vector_store.create_collection():
            logger.error("Failed to create Qdrant collection")
            sys.exit(1)

        # Crawl the website
        logger.info("Starting website crawling...")
        crawled_pages = crawler.crawl_website()
        logger.info(f"Crawling completed. Found {len(crawled_pages)} pages.")

        # Process and store embeddings
        all_embeddings = []
        total_chunks = 0

        for i, page in enumerate(crawled_pages):
            logger.info(f"Processing page {i+1}/{len(crawled_pages)}: {page['url']}")

            # Process the content
            chunks = text_processor.process_content(
                page['content'],
                url=page['url'],
                heading=page.get('title', '')
            )
            total_chunks += len(chunks)

            # Generate embeddings for all chunks
            if chunks:
                texts_to_embed = [chunk.content for chunk in chunks]
                embeddings = embedder.embed_texts(texts_to_embed)

                # Prepare embeddings for storage with metadata
                for j, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                    embedding_data = {
                        'vector': embedding,
                        'url': chunk.url,
                        'section': chunk.section,
                        'heading': chunk.heading,
                        'chunk_index': chunk.chunk_index,
                        'content': chunk.content
                    }
                    all_embeddings.append(embedding_data)

                logger.info(f"Generated {len(embeddings)} embeddings for page {i+1}")

        # Store all embeddings in Qdrant
        logger.info(f"Storing {len(all_embeddings)} embeddings in Qdrant Cloud...")
        if vector_store.store_embeddings(all_embeddings):
            logger.info("Embeddings successfully stored in Qdrant Cloud")
        else:
            logger.error("Failed to store embeddings in Qdrant Cloud")
            sys.exit(1)

        # Verify the embeddings are stored correctly
        logger.info("Verifying embeddings in Qdrant Cloud...")
        if vector_store.verify_embeddings():
            logger.info("Embeddings verification successful")
        else:
            logger.warning("Embeddings verification had issues")

        # Print final statistics
        total_stored = vector_store.get_total_count()
        logger.info(f"Pipeline completed successfully!")
        logger.info(f"- Pages crawled: {len(crawled_pages)}")
        logger.info(f"- Text chunks processed: {total_chunks}")
        logger.info(f"- Embeddings generated: {len(all_embeddings)}")
        logger.info(f"- Embeddings stored: {total_stored}")

    except KeyboardInterrupt:
        logger.info("Pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Pipeline failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()