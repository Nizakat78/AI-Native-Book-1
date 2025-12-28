"""Text processing module for cleaning and chunking content."""

import re
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class TextChunk:
    """Represents a chunk of text with metadata."""
    content: str
    url: str
    section: str
    heading: str
    chunk_index: int


class TextProcessor:
    """Processor for cleaning and chunking text content."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 100):
        """
        Initialize the text processor.

        Args:
            chunk_size: Maximum size of each text chunk
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def clean_text(self, text: str) -> str:
        """
        Clean text by removing extra whitespace and normalizing content.

        Args:
            text: Raw text content to clean

        Returns:
            Cleaned text
        """
        if not text:
            return ""

        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()

        # Remove special characters that might interfere with embeddings
        # Keep letters, numbers, punctuation, and common symbols
        text = re.sub(r'[^\w\s\-\.\,\!\?\;\:\(\)\[\]\{\}\'\"\/\\]', ' ', text)
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace again after cleaning

        return text

    def chunk_text(self, text: str, url: str = "", heading: str = "") -> List[TextChunk]:
        """
        Split text into overlapping chunks of specified size.

        Args:
            text: Text content to chunk
            url: URL associated with the text
            heading: Heading associated with the text

        Returns:
            List of TextChunk objects
        """
        if not text:
            return []

        chunks = []
        start = 0
        chunk_index = 0

        while start < len(text):
            # Determine the end position for this chunk
            end = start + self.chunk_size

            # If this is not the last chunk, try to break at a sentence or word boundary
            if end < len(text):
                # Look for a good break point (sentence end, then word boundary)
                search_start = end - 50  # Search in the last 50 characters
                if search_start < start:
                    search_start = start

                # First, try to find a sentence boundary
                sentence_break = -1
                for i in range(min(end, len(text)) - 1, search_start, -1):
                    if text[i] in '.!?':
                        sentence_break = i + 1
                        break

                if sentence_break != -1:
                    end = sentence_break
                else:
                    # If no sentence boundary found, look for a word boundary
                    for i in range(min(end, len(text)) - 1, search_start, -1):
                        if text[i] in ' \t\n\r':
                            end = i
                            break

            # Extract the chunk
            chunk_content = text[start:end].strip()

            if chunk_content:  # Only add non-empty chunks
                chunk = TextChunk(
                    content=chunk_content,
                    url=url,
                    section=url.split('/')[-1] if url else "unknown",
                    heading=heading,
                    chunk_index=chunk_index
                )
                chunks.append(chunk)

            # Move to the next chunk position
            start = end - self.chunk_overlap if self.chunk_overlap < end else end
            chunk_index += 1

        return chunks

    def process_content(self, content: str, url: str = "", heading: str = "") -> List[TextChunk]:
        """
        Process content by cleaning and chunking.

        Args:
            content: Raw content to process
            url: URL associated with the content
            heading: Heading associated with the content

        Returns:
            List of processed TextChunk objects
        """
        cleaned_content = self.clean_text(content)
        chunks = self.chunk_text(cleaned_content, url, heading)
        return chunks

    def extract_headings(self, html: str) -> List[Dict[str, str]]:
        """
        Extract headings from HTML content.

        Args:
            html: HTML content to extract headings from

        Returns:
            List of dictionaries with heading level and text
        """
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        headings = []
        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            headings.append({
                'level': heading.name,
                'text': heading.get_text().strip(),
                'id': heading.get('id', '')
            })

        return headings