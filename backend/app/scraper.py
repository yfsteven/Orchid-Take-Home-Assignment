import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import logging
from urllib.parse import urlparse, urljoin

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def scrape_website(self, url: str) -> Dict:
        """
        Scrape a website and return its structure and content.
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract basic metadata
            metadata = {
                'title': self._get_title(soup),
                'description': self._get_description(soup),
                'favicon': self._get_favicon(soup, url),
                'color_scheme': self._extract_color_scheme(soup),
                'fonts': self._extract_fonts(soup),
            }
            
            # Extract layout structure
            layout = {
                'header': self._extract_section(soup, 'header'),
                'main': self._extract_section(soup, 'main'),
                'footer': self._extract_section(soup, 'footer'),
                'navigation': self._extract_navigation(soup),
            }
            
            # Extract styles
            styles = {
                'css': self._extract_css(soup),
                'inline_styles': self._extract_inline_styles(soup),
            }
            
            return {
                'url': url,
                'metadata': metadata,
                'layout': layout,
                'styles': styles,
                'raw_html': response.text
            }
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            raise

    def _get_title(self, soup: BeautifulSoup) -> str:
        """Extract the page title."""
        title_tag = soup.find('title')
        return title_tag.text.strip() if title_tag else ''

    def _get_description(self, soup: BeautifulSoup) -> str:
        """Extract the page description."""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        return meta_desc['content'] if meta_desc else ''

    def _get_favicon(self, soup: BeautifulSoup, base_url: str) -> str:
        """Extract the favicon URL."""
        favicon = soup.find('link', rel='icon') or soup.find('link', rel='shortcut icon')
        if favicon and 'href' in favicon.attrs:
            return urljoin(base_url, favicon['href'])
        return ''

    def _extract_color_scheme(self, soup: BeautifulSoup) -> List[str]:
        """Extract the main colors used in the website."""
        colors = set()
        for style in soup.find_all('style'):
            # Basic color extraction from CSS
            if style.string:
                colors.update(self._extract_colors_from_css(style.string))
        return list(colors)

    def _extract_colors_from_css(self, css: str) -> List[str]:
        """Extract color values from CSS."""
        import re
        color_patterns = [
            r'#[0-9a-fA-F]{3,6}',  # Hex colors
            r'rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)',  # RGB colors
            r'rgba\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*[\d.]+\s*\)'  # RGBA colors
        ]
        colors = set()
        for pattern in color_patterns:
            colors.update(re.findall(pattern, css))
        return list(colors)

    def _extract_fonts(self, soup: BeautifulSoup) -> List[str]:
        """Extract the fonts used in the website."""
        fonts = set()
        for style in soup.find_all('style'):
            if style.string:
                fonts.update(self._extract_fonts_from_css(style.string))
        return list(fonts)

    def _extract_fonts_from_css(self, css: str) -> List[str]:
        """Extract font families from CSS."""
        import re
        font_pattern = r'font-family:\s*([^;]+)'
        fonts = set()
        for match in re.finditer(font_pattern, css):
            font_list = match.group(1).split(',')
            fonts.update(f.strip().strip("'").strip('"') for f in font_list)
        return list(fonts)

    def _extract_section(self, soup: BeautifulSoup, section: str) -> Dict:
        """Extract content from a specific section."""
        section_elem = soup.find(section)
        if not section_elem:
            return {}
            
        return {
            'content': section_elem.get_text(strip=True),
            'html': str(section_elem),
            'classes': section_elem.get('class', []),
            'id': section_elem.get('id', '')
        }

    def _extract_navigation(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract navigation menu structure."""
        nav_items = []
        nav = soup.find('nav')
        if nav:
            for link in nav.find_all('a'):
                nav_items.append({
                    'text': link.get_text(strip=True),
                    'href': link.get('href', ''),
                    'classes': link.get('class', [])
                })
        return nav_items

    def _extract_css(self, soup: BeautifulSoup) -> List[str]:
        """Extract external CSS files."""
        css_files = []
        for link in soup.find_all('link', rel='stylesheet'):
            if 'href' in link.attrs:
                css_files.append(link['href'])
        return css_files

    def _extract_inline_styles(self, soup: BeautifulSoup) -> List[str]:
        """Extract inline styles."""
        styles = []
        for style in soup.find_all('style'):
            if style.string:
                styles.append(style.string.strip())
        return styles 