import asyncio
import aiohttp
import base64
from typing import Dict, Any, List, Optional
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import json

class WebsiteScraper:
    """Advanced website scraper with design context extraction"""
    
    def __init__(self):
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def scrape(self, url: str) -> Dict[str, Any]:
        """Scrape website and extract comprehensive design context"""
        try:
            # Fetch main page
            html = await self._fetch_url(url)
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract various design elements
            design_context = {
                "url": url,
                "domain": urlparse(url).netloc,
                "title": self._extract_title(soup),
                "meta": self._extract_meta_tags(soup),
                "structure": self._analyze_structure(soup),
                "typography": self._extract_typography(soup),
                "colors": await self._extract_colors(soup, url),
                "layout": self._analyze_layout(soup),
                "images": self._extract_images(soup, url),
                "navigation": self._extract_navigation(soup),
                "stylesheets": await self._extract_stylesheets(soup, url),
                "components": self._identify_components(soup),
                "responsive": self._check_responsive_design(soup),
                "features": self._detect_features(soup)
            }
            
            return design_context
            
        except Exception as e:
            raise Exception(f"Scraping failed: {str(e)}")
    
    async def _fetch_url(self, url: str, timeout: int = 30) -> str:
        """Fetch URL content"""
        async with self.session.get(url, timeout=timeout) as response:
            response.raise_for_status()
            return await response.text()
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""
        title_tag = soup.find('title')
        return title_tag.text.strip() if title_tag else "Untitled"
    
    def _extract_meta_tags(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract important meta tags"""
        meta_tags = {}
        
        # Common meta tags to extract
        meta_names = ['description', 'keywords', 'author', 'viewport', 'theme-color']
        
        for name in meta_names:
            tag = soup.find('meta', attrs={'name': name})
            if tag and tag.get('content'):
                meta_tags[name] = tag['content']
        
        # Open Graph tags
        og_tags = soup.find_all('meta', attrs={'property': re.compile('^og:')})
        for tag in og_tags:
            if tag.get('content'):
                meta_tags[tag['property']] = tag['content']
        
        return meta_tags
    
    def _analyze_structure(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze page structure"""
        structure = {
            "has_header": bool(soup.find(['header', 'nav'])),
            "has_footer": bool(soup.find('footer')),
            "has_sidebar": bool(soup.find(['aside', '[class*="sidebar"]', '[id*="sidebar"]'])),
            "main_sections": len(soup.find_all(['section', 'article'])),
            "heading_hierarchy": self._analyze_headings(soup),
            "semantic_elements": self._count_semantic_elements(soup)
        }
        return structure
    
    def _analyze_headings(self, soup: BeautifulSoup) -> Dict[str, int]:
        """Analyze heading hierarchy"""
        headings = {}
        for i in range(1, 7):
            headings[f'h{i}'] = len(soup.find_all(f'h{i}'))
        return headings
    
    def _count_semantic_elements(self, soup: BeautifulSoup) -> Dict[str, int]:
        """Count semantic HTML5 elements"""
        semantic_tags = ['header', 'nav', 'main', 'article', 'section', 'aside', 'footer']
        return {tag: len(soup.find_all(tag)) for tag in semantic_tags}
    
    def _extract_typography(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract typography information"""
        typography = {
            "fonts": [],
            "font_sizes": [],
            "line_heights": [],
            "font_weights": []
        }
        
        # Extract from inline styles
        style_tags = soup.find_all('style')
        for style in style_tags:
            text = style.string or ""
            
            # Extract font families
            fonts = re.findall(r'font-family:\s*([^;]+);', text)
            typography['fonts'].extend(fonts)
            
            # Extract font sizes
            sizes = re.findall(r'font-size:\s*([^;]+);', text)
            typography['font_sizes'].extend(sizes)
        
        # Remove duplicates
        typography['fonts'] = list(set(typography['fonts']))[:5]
        typography['font_sizes'] = list(set(typography['font_sizes']))[:10]
        
        return typography
    
    async def _extract_colors(self, soup: BeautifulSoup, base_url: str) -> Dict[str, Any]:
        """Extract color palette from styles"""
        colors = {
            "primary": [],
            "background": [],
            "text": [],
            "all_colors": []
        }
        
        # Extract from inline styles
        style_tags = soup.find_all('style')
        for style in style_tags:
            text = style.string or ""
            
            # Extract hex colors
            hex_colors = re.findall(r'#[0-9a-fA-F]{3,8}', text)
            colors['all_colors'].extend(hex_colors)
            
            # Extract rgb/rgba colors
            rgb_colors = re.findall(r'rgba?\([^)]+\)', text)
            colors['all_colors'].extend(rgb_colors)
            
            # Categorize colors
            if 'background' in text:
                bg_colors = re.findall(r'background(?:-color)?:\s*([^;]+);', text)
                colors['background'].extend(bg_colors)
            
            if 'color:' in text:
                text_colors = re.findall(r'(?<!background-)color:\s*([^;]+);', text)
                colors['text'].extend(text_colors)
        
        # Remove duplicates and limit
        for key in colors:
            colors[key] = list(set(colors[key]))[:10]
        
        return colors
    
    def _analyze_layout(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze page layout"""
        layout = {
            "container_classes": [],
            "grid_system": "unknown",
            "max_width": None,
            "layout_type": "unknown"
        }
        
        # Look for common container classes
        containers = soup.find_all(class_=re.compile(r'container|wrapper|content|main'))
        layout['container_classes'] = list(set([c.get('class', [''])[0] for c in containers[:5]]))
        
        # Detect grid systems
        if soup.find(class_=re.compile(r'col-|column-|grid-')):
            layout['grid_system'] = "grid-based"
        elif soup.find(class_=re.compile(r'flex|flexbox')):
            layout['grid_system'] = "flexbox"
        
        # Detect layout type
        if soup.find(class_=re.compile(r'sidebar|aside')):
            layout['layout_type'] = "sidebar"
        elif len(soup.find_all(['section', 'article'])) > 3:
            layout['layout_type'] = "multi-section"
        else:
            layout['layout_type'] = "single-column"
        
        return layout
    
    def _extract_images(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
        """Extract image information"""
        images = []
        img_tags = soup.find_all('img')[:10]  # Limit to first 10 images
        
        for img in img_tags:
            img_data = {
                "src": urljoin(base_url, img.get('src', '')),
                "alt": img.get('alt', ''),
                "width": img.get('width', 'auto'),
                "height": img.get('height', 'auto'),
                "class": ' '.join(img.get('class', []))
            }
            images.append(img_data)
        
        return images
    
    def _extract_navigation(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract navigation structure"""
        navigation = {
            "menu_items": [],
            "has_dropdown": False,
            "is_sticky": False,
            "position": "top"
        }
        
        # Find navigation elements
        nav = soup.find(['nav', '[role="navigation"]'])
        if nav:
            # Extract menu items
            links = nav.find_all('a')[:10]
            navigation['menu_items'] = [
                {"text": link.text.strip(), "href": link.get('href', '#')}
                for link in links
            ]
            
            # Check for dropdowns
            navigation['has_dropdown'] = bool(nav.find(class_=re.compile(r'dropdown|submenu')))
            
            # Check if sticky
            nav_classes = ' '.join(nav.get('class', []))
            navigation['is_sticky'] = 'sticky' in nav_classes or 'fixed' in nav_classes
        
        return navigation
    
    async def _extract_stylesheets(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, Any]]:
        """Extract and analyze external stylesheets"""
        stylesheets = []
        link_tags = soup.find_all('link', rel='stylesheet')[:5]  # Limit to 5 stylesheets
        
        for link in link_tags:
            href = link.get('href')
            if href:
                stylesheet = {
                    "href": urljoin(base_url, href),
                    "media": link.get('media', 'all'),
                    "type": "external"
                }
                
                # Try to fetch and analyze stylesheet
                try:
                    css_url = urljoin(base_url, href)
                    css_content = await self._fetch_url(css_url, timeout=10)
                    stylesheet['size'] = len(css_content)
                    stylesheet['has_responsive'] = '@media' in css_content
                except:
                    pass
                
                stylesheets.append(stylesheet)
        
        return stylesheets
    
    def _identify_components(self, soup: BeautifulSoup) -> Dict[str, bool]:
        """Identify common UI components"""
        components = {
            "hero_section": bool(soup.find(class_=re.compile(r'hero|banner|jumbotron'))),
            "cards": bool(soup.find(class_=re.compile(r'card|tile|box'))),
            "carousel": bool(soup.find(class_=re.compile(r'carousel|slider|swiper'))),
            "modal": bool(soup.find(class_=re.compile(r'modal|popup|dialog'))),
            "tabs": bool(soup.find(class_=re.compile(r'tab|tabs'))),
            "accordion": bool(soup.find(class_=re.compile(r'accordion|collapse'))),
            "forms": bool(soup.find('form')),
            "tables": bool(soup.find('table')),
            "video": bool(soup.find(['video', 'iframe'])),
            "social_links": bool(soup.find(href=re.compile(r'facebook|twitter|instagram|linkedin')))
        }
        return components
    
    def _check_responsive_design(self, soup: BeautifulSoup) -> Dict[str, bool]:
        """Check for responsive design indicators"""
        responsive = {
            "has_viewport_meta": False,
            "uses_responsive_images": False,
            "has_mobile_menu": False
        }
        
        # Check viewport meta
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        responsive['has_viewport_meta'] = bool(viewport)
        
        # Check for responsive images
        responsive['uses_responsive_images'] = bool(
            soup.find('img', srcset=True) or 
            soup.find('picture')
        )
        
        # Check for mobile menu indicators
        responsive['has_mobile_menu'] = bool(
            soup.find(class_=re.compile(r'mobile-menu|hamburger|menu-toggle'))
        )
        
        return responsive
    
    def _detect_features(self, soup: BeautifulSoup) -> List[str]:
        """Detect special features and technologies"""
        features = []
        
        # Common feature detection
        if soup.find(class_=re.compile(r'dark-mode|dark-theme')):
            features.append("dark_mode")
        
        if soup.find(['[data-aos]', '[data-scroll]']):
            features.append("scroll_animations")
        
        if soup.find(class_=re.compile(r'lazy|lazyload')):
            features.append("lazy_loading")
        
        if soup.find('script', string=re.compile(r'gtag|analytics|_gaq')):
            features.append("analytics")
        
        if soup.find(class_=re.compile(r'search|search-box')):
            features.append("search_functionality")
        
        return features

# Utility function for use in main.py
async def scrape_website_advanced(url: str) -> Dict[str, Any]:
    """Advanced website scraping with comprehensive design extraction"""
    async with WebsiteScraper() as scraper:
        return await scraper.scrape(url)