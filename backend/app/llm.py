import openai
from typing import Dict, List, Optional
import logging
import json
from pathlib import Path
import os
from dotenv import load_dotenv
import httpx

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

    def generate_website_code(self, scraped_data: Dict) -> Dict:
        """
        Generate website code based on scraped data using LLM.
        """
        try:
            # Prepare the prompt
            prompt = self._create_prompt(scraped_data)
            logger.info("Sending request to OpenAI API...")
            
            # Call the LLM using the new OpenAI API client
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a web development expert. Generate modern, responsive website code based on the provided design data."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            logger.info("Received response from OpenAI API")
            # Parse the response using the new API response structure
            generated_code = response.choices[0].message.content
            
            # Extract HTML, CSS, and JavaScript
            return self._parse_generated_code(generated_code)
            
        except Exception as e:
            logger.error(f"Error generating website code: {str(e)}")
            raise

    def _create_prompt(self, scraped_data: Dict) -> str:
        """Create a prompt for the LLM based on scraped data."""
        prompt = f"""
        Generate a modern, responsive website based on the following design data:
        
        URL: {scraped_data['url']}
        
        Metadata:
        - Title: {scraped_data['metadata']['title']}
        - Description: {scraped_data['metadata']['description']}
        
        Color Scheme: {', '.join(scraped_data['metadata']['color_scheme'])}
        Fonts: {', '.join(scraped_data['metadata']['fonts'])}
        
        Layout Structure:
        {json.dumps(scraped_data['layout'], indent=2)}
        
        Please generate:
        1. HTML structure
        2. CSS styles (including responsive design)
        3. JavaScript for interactivity
        
        The code should be modern, clean, and follow best practices.
        """
        return prompt

    def _parse_generated_code(self, code: str) -> Dict:
        """Parse the generated code into HTML, CSS, and JavaScript components."""
        # Basic parsing logic - can be enhanced based on actual LLM output format
        sections = {
            'html': '',
            'css': '',
            'javascript': ''
        }
        
        current_section = None
        for line in code.split('\n'):
            if line.strip().startswith('<!-- HTML -->'):
                current_section = 'html'
            elif line.strip().startswith('/* CSS */'):
                current_section = 'css'
            elif line.strip().startswith('// JavaScript'):
                current_section = 'javascript'
            elif current_section:
                sections[current_section] += line + '\n'
        
        return sections

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