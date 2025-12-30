"""Web crawler module for extracting content from Docusaurus websites."""

import time
import requests
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)


class Crawler:
    """Crawler for Docusaurus documentation websites."""

    def __init__(self, base_url: str, delay_between_requests: float = 1.0, max_retries: int = 3):
        """
        Initialize the crawler.

        Args:
            base_url: The base URL of the Docusaurus website to crawl
            delay_between_requests: Delay in seconds between requests to be respectful
            max_retries: Maximum number of retries for failed requests
        """
        self.base_url = base_url
        self.delay_between_requests = delay_between_requests
        self.max_retries = max_retries

        # Create session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; RAG-Crawler/1.0; +https://github.com/your-repo)'
        })

    def get_page(self, url: str) -> Optional[str]:
        """
        Fetch a single page and return its HTML content.

        Args:
            url: The URL to fetch

        Returns:
            HTML content as string, or None if request failed
        """
        try:
            time.sleep(self.delay_between_requests)  # Be respectful to the server
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None

    def extract_links(self, html: str) -> List[str]:
        """
        Extract all internal links from the HTML content.

        Args:
            html: HTML content to extract links from

        Returns:
            List of URLs found in the HTML
        """
        soup = BeautifulSoup(html, 'html.parser')
        links = set()
        base_domain = urlparse(self.base_url).netloc

        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(self.base_url, href)

            # Only include internal links to the same domain
            if urlparse(full_url).netloc == base_domain:
                links.add(full_url)

        return list(links)

    def get_urls_from_sitemap(self) -> List[str]:
        """
        Fetch and parse URLs from the website's sitemap.xml file.

        Returns:
            List of URLs extracted from sitemap.xml
        """
        sitemap_url = urljoin(self.base_url, 'sitemap.xml')
        logger.info(f"Fetching sitemap from: {sitemap_url}")

        try:
            response = self.session.get(sitemap_url, timeout=30)
            response.raise_for_status()

            # Parse the XML content
            root = ET.fromstring(response.content)

            # Extract URLs from the sitemap
            urls = []
            # Handle both regular sitemap and sitemap index
            if 'sitemapindex' in root.tag:
                # This is a sitemap index, need to fetch individual sitemaps
                for sitemap_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap/{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                    if sitemap_elem is not None:
                        individual_sitemap_url = sitemap_elem.text
                        logger.info(f"Found sitemap: {individual_sitemap_url}")
                        # Fetch and parse individual sitemap
                        individual_response = self.session.get(individual_sitemap_url, timeout=30)
                        individual_response.raise_for_status()
                        individual_root = ET.fromstring(individual_response.content)
                        for url_elem in individual_root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                            if url_elem is not None:
                                # Fix the URL by replacing the placeholder domain with the actual base URL
                                original_url = url_elem.text
                                # Parse the original URL to extract the path
                                parsed_original = urlparse(original_url)
                                # Use the base URL's domain but keep the original path
                                fixed_url = urljoin(self.base_url, parsed_original.path.lstrip('/'))
                                urls.append(fixed_url)
            else:
                # This is a regular sitemap with URLs
                for url_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                    if url_elem is not None:
                        # Fix the URL by replacing the placeholder domain with the actual base URL
                        original_url = url_elem.text
                        # Parse the original URL to extract the path
                        parsed_original = urlparse(original_url)
                        # Use the base URL's domain but keep the original path
                        fixed_url = urljoin(self.base_url, parsed_original.path.lstrip('/'))
                        urls.append(fixed_url)

            logger.info(f"Extracted {len(urls)} URLs from sitemap")
            return urls
        except requests.RequestException as e:
            logger.error(f"Failed to fetch sitemap from {sitemap_url}: {e}")
            return []
        except ET.ParseError as e:
            logger.error(f"Failed to parse sitemap XML from {sitemap_url}: {e}")
            return []

    def crawl_website(self, max_pages: Optional[int] = None) -> List[Dict[str, str]]:
        """
        Crawl the website by fetching URLs from sitemap.xml instead of following links.

        Args:
            max_pages: Maximum number of pages to crawl (None for unlimited)

        Returns:
            List of dictionaries with 'url' and 'content' keys
        """
        # Get URLs from sitemap
        sitemap_urls = self.get_urls_from_sitemap()

        if not sitemap_urls:
            logger.warning("No URLs found in sitemap, falling back to link following method")
            # Fallback to the original approach
            visited_urls = set()
            to_visit = [self.base_url]
            crawled_pages = []

            while to_visit and (max_pages is None or len(crawled_pages) < max_pages):
                current_url = to_visit.pop(0)

                if current_url in visited_urls:
                    continue

                visited_urls.add(current_url)
                logger.info(f"Crawling: {current_url}")

                html_content = self.get_page(current_url)
                if html_content:
                    # Extract links for further crawling
                    new_links = self.extract_links(html_content)
                    for link in new_links:
                        if link not in visited_urls and link not in to_visit:
                            to_visit.append(link)

                    # Extract clean text content
                    text_content = self.extract_text_from_html(html_content)
                    crawled_pages.append({
                        'url': current_url,
                        'title': self.extract_title_from_html(html_content),
                        'content': text_content
                    })
        else:
            # Use sitemap URLs
            crawled_pages = []
            urls_to_crawl = sitemap_urls[:max_pages] if max_pages else sitemap_urls

            for i, current_url in enumerate(urls_to_crawl):
                # Skip anchor links (URLs with fragments)
                if '#' in current_url:
                    logger.info(f"Skipping anchor link: {current_url}")
                    continue

                logger.info(f"Crawling ({i+1}/{len(urls_to_crawl)}): {current_url}")

                html_content = self.get_page(current_url)
                if html_content:
                    # Extract clean text content
                    text_content = self.extract_text_from_html(html_content)
                    crawled_pages.append({
                        'url': current_url,
                        'title': self.extract_title_from_html(html_content),
                        'content': text_content
                    })

        logger.info(f"Crawling completed. Processed {len(crawled_pages)} pages.")
        return crawled_pages

    def extract_text_from_html(self, html: str) -> str:
        """
        Extract clean text content from HTML, removing navigation and other non-content elements.

        Args:
            html: HTML content to extract text from

        Returns:
            Clean text content
        """
        soup = BeautifulSoup(html, 'html.parser')

        # Remove navigation elements that are common in Docusaurus sites
        for element in soup(['nav', 'header', 'footer', 'aside']):
            element.decompose()

        # Remove script and style elements
        for element in soup(['script', 'style', 'meta', 'link']):
            element.decompose()

        # Try to find main content area (Docusaurus specific selectors)
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='container') or soup

        # Get text and clean it up
        text = main_content.get_text(separator=' ')
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split('  '))
        text = ' '.join(chunk for chunk in chunks if chunk)

        return text

    def extract_title_from_html(self, html: str) -> str:
        """
        Extract the title from HTML content.

        Args:
            html: HTML content to extract title from

        Returns:
            Title string
        """
        soup = BeautifulSoup(html, 'html.parser')
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text().strip()

        # Fallback: try to find h1
        h1_tag = soup.find('h1')
        if h1_tag:
            return h1_tag.get_text().strip()

        return "Untitled Page"