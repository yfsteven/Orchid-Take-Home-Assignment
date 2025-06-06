import json
import time
from typing import Dict

class LLM:
    def _truncate_text(self, text: str, max_chars: int = 2000) -> str:
        """Truncate text to a maximum number of characters, adding ellipsis if needed."""
        if len(text) > max_chars:
            return text[:max_chars] + "... [truncated]"
        return text

    def _truncate_json(self, data, max_chars: int = 2000) -> str:
        """Truncate a JSON-serializable object to a string of max_chars."""
        s = json.dumps(data, indent=2)
        return self._truncate_text(s, max_chars)

    def _create_html_prompt(self, scraped_data: Dict) -> str:
        """Create a prompt for HTML generation, truncating large fields."""
        return f"""
        Generate a clean, semantic HTML structure for a website based on:
        
        Title: {self._truncate_text(scraped_data['metadata'].get('title', ''), 200)}
        Description: {self._truncate_text(scraped_data['metadata'].get('description', ''), 400)}
        
        Layout Structure:
        - Header: {self._truncate_json(scraped_data['layout'].get('header', {}), 600)}
        - Navigation: {self._truncate_json(scraped_data['layout'].get('navigation', {}), 600)}
        - Main Content: {self._truncate_json(scraped_data['layout'].get('main', {}), 1000)}
        - Footer: {self._truncate_json(scraped_data['layout'].get('footer', {}), 600)}
        
        Focus on semantic HTML5 elements and accessibility.
        """

    def _create_css_prompt(self, scraped_data: Dict) -> str:
        """Create a prompt for CSS generation, truncating large fields."""
        return f"""
        Generate modern, responsive CSS styles for a website based on:
        
        Color Scheme: {', '.join(scraped_data['metadata'].get('color_scheme', [])[:10])}
        Fonts: {', '.join(scraped_data['metadata'].get('fonts', [])[:5])}
        
        Include:
        1. Reset/normalize styles
        2. Responsive grid system
        3. Typography styles
        4. Component styles
        5. Media queries for mobile responsiveness
        """

    def _create_js_prompt(self, scraped_data: Dict) -> str:
        """Create a prompt for JavaScript generation, truncating large fields."""
        return f"""
        Generate modern JavaScript code for a website based on:
        
        Layout Structure:
        {self._truncate_json(scraped_data['layout'], 1200)}
        
        Include:
        1. Navigation functionality
        2. Smooth scrolling
        3. Responsive menu
        4. Any interactive elements
        """

    def generate_website_code(self, scraped_data: Dict) -> Dict:
        """
        Generate website code based on scraped data using LLM.
        Truncate or chunk data to avoid exceeding context length.
        """
        try:
            # Truncate raw_html and styles if present
            if 'raw_html' in scraped_data:
                scraped_data['raw_html'] = self._truncate_text(scraped_data['raw_html'], 2000)
            if 'styles' in scraped_data and 'inline_styles' in scraped_data['styles']:
                scraped_data['styles']['inline_styles'] = [self._truncate_text(s, 1000) for s in scraped_data['styles']['inline_styles']]

            # Generate HTML first
            html_prompt = self._create_html_prompt(scraped_data)
            logger.info("Generating HTML structure...")
            html_code = self._call_openai([
                {"role": "system", "content": "You are a web development expert. Generate clean, semantic HTML structure based on the provided design data."},
                {"role": "user", "content": html_prompt}
            ])

            time.sleep(1)

            # Generate CSS
            css_prompt = self._create_css_prompt(scraped_data)
            logger.info("Generating CSS styles...")
            css_code = self._call_openai([
                {"role": "system", "content": "You are a CSS expert. Generate modern, responsive CSS styles based on the provided design data."},
                {"role": "user", "content": css_prompt}
            ])

            time.sleep(1)

            # Generate JavaScript
            js_prompt = self._create_js_prompt(scraped_data)
            logger.info("Generating JavaScript...")
            js_code = self._call_openai([
                {"role": "system", "content": "You are a JavaScript expert. Generate clean, modern JavaScript code for interactivity based on the provided design data."},
                {"role": "user", "content": js_prompt}
            ])

            return {
                'html': html_code,
                'css': css_code,
                'javascript': js_code
            }
        except Exception as e:
            logger.error(f"Error generating website code: {str(e)}")
            raise 