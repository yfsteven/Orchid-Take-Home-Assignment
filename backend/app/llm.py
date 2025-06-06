import openai
from typing import Dict, List, Optional
import logging
import json
from pathlib import Path
import os
from dotenv import load_dotenv
import httpx
import time
from tenacity import retry, stop_after_attempt, wait_exponential

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class LLMGenerator:
    def __init__(self, api_key: Optional[str] = None):
        # Hardcoded API key
        self.api_key = "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"
            
        logger.info(f"Initializing LLMGenerator with API key length: {len(self.api_key)}")
        
        try:
            # Initialize OpenAI client with minimal configuration
            self.client = openai.OpenAI(
                api_key=self.api_key,
                http_client=httpx.Client()
            )
            logger.info("OpenAI client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {str(e)}")
            raise

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=5, min=10, max=120))
    def _call_openai(self, messages: List[Dict], max_tokens: int = 1000) -> str:
        """Make an API call to OpenAI with retries and longer delays."""
        try:
            # Add a delay before each attempt to avoid rate limits
            time.sleep(5)
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API call failed: {str(e)}")
            # Add extra delay on error
            time.sleep(10)
            raise

    def _truncate_text(self, text: str, max_chars: int = 500) -> str:
        """Truncate text to a maximum number of characters, adding ellipsis if needed."""
        if len(text) > max_chars:
            return text[:max_chars] + "... [truncated]"
        return text

    def _truncate_json(self, data, max_chars: int = 500) -> str:
        """Truncate a JSON-serializable object to a string of max_chars."""
        s = json.dumps(data, indent=2)
        return self._truncate_text(s, max_chars)

    def generate_website_code(self, scraped_data: Dict) -> Dict:
        """
        Generate website code based on scraped data using LLM.
        Truncate or chunk data to avoid exceeding context length.
        """
        try:
            # Truncate raw_html and styles if present
            if 'raw_html' in scraped_data:
                scraped_data['raw_html'] = self._truncate_text(scraped_data['raw_html'], 500)
            if 'styles' in scraped_data and 'inline_styles' in scraped_data['styles']:
                scraped_data['styles']['inline_styles'] = [self._truncate_text(s, 250) for s in scraped_data['styles']['inline_styles']]

            # Generate HTML first
            html_prompt = self._create_html_prompt(scraped_data)
            logger.info("Generating HTML structure...")
            html_code = self._call_openai([
                {"role": "system", "content": "You are a web development expert. Generate clean, semantic HTML structure based on the provided design data."},
                {"role": "user", "content": html_prompt}
            ])

            time.sleep(5)  # Increased delay between calls

            # Generate CSS
            css_prompt = self._create_css_prompt(scraped_data)
            logger.info("Generating CSS styles...")
            css_code = self._call_openai([
                {"role": "system", "content": "You are a CSS expert. Generate modern, responsive CSS styles based on the provided design data."},
                {"role": "user", "content": css_prompt}
            ])

            time.sleep(5)  # Increased delay between calls

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

    def _create_html_prompt(self, scraped_data: Dict) -> str:
        """Create a prompt for HTML generation, truncating large fields."""
        return f"""
        Generate a clean, semantic HTML structure for a website based on:
        
        Title: {self._truncate_text(scraped_data['metadata'].get('title', ''), 50)}
        Description: {self._truncate_text(scraped_data['metadata'].get('description', ''), 100)}
        
        Layout Structure:
        - Header: {self._truncate_json(scraped_data['layout'].get('header', {}), 150)}
        - Navigation: {self._truncate_json(scraped_data['layout'].get('navigation', {}), 150)}
        - Main Content: {self._truncate_json(scraped_data['layout'].get('main', {}), 250)}
        - Footer: {self._truncate_json(scraped_data['layout'].get('footer', {}), 150)}
        
        Focus on semantic HTML5 elements and accessibility.
        """

    def _create_css_prompt(self, scraped_data: Dict) -> str:
        """Create a prompt for CSS generation, truncating large fields."""
        return f"""
        Generate modern, responsive CSS styles for a website based on:
        
        Color Scheme: {', '.join(scraped_data['metadata'].get('color_scheme', [])[:3])}
        Fonts: {', '.join(scraped_data['metadata'].get('fonts', [])[:2])}
        
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
        {self._truncate_json(scraped_data['layout'], 300)}
        
        Include:
        1. Navigation functionality
        2. Smooth scrolling
        3. Responsive menu
        4. Any interactive elements
        """

    def save_generated_code(self, code: Dict, output_dir: str):
        """Save the generated code to files."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save HTML
        with open(output_path / 'index.html', 'w') as f:
            f.write(code['html'])
        
        # Save CSS
        with open(output_path / 'styles.css', 'w') as f:
            f.write(code['css'])
        
        # Save JavaScript
        with open(output_path / 'script.js', 'w') as f:
            f.write(code['javascript']) 