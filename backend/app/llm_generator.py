import json
from typing import Dict, Any
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

async def generate_html_clone(scrape_data: Dict[str, Any]) -> str:
    """Generate HTML clone using Claude AI based on scraped data"""
    try:
        prompt = _create_prompt(scrape_data)
        html = await _call_claude_api(prompt)
        return html
    except Exception as e:
        raise Exception(f"Failed to generate HTML: {str(e)}")

def _create_prompt(scrape_data: Dict[str, Any]) -> str:
    prompt = f"""
You are an expert web developer. Given the following website design context, generate a complete, production-ready, responsive HTML file that closely matches the original site's look and feel. Use modern HTML5, CSS3, and semantic elements. Include all CSS in a <style> tag in the <head>. Make sure the result is mobile-friendly and includes meta tags for SEO and viewport.

Title: {scrape_data['title']}

Design Context:
- Colors: {json.dumps(scrape_data['colors'], indent=2)}
- Layout: {json.dumps(scrape_data['layout'], indent=2)}
- Components: {json.dumps(scrape_data['components'], indent=2)}
- Typography: {json.dumps(scrape_data['typography'], indent=2)}
- Structure: {json.dumps(scrape_data['structure'], indent=2)}

Requirements:
1. Use modern HTML5 and CSS3
2. Make it fully responsive
3. Include all necessary CSS in a <style> tag
4. Use semantic HTML elements
5. Include meta tags for SEO
6. Add viewport meta tag for mobile responsiveness
7. Include necessary JavaScript for interactivity (if any)
8. Use the exact color scheme from the original
9. Match the layout structure precisely
10. Include all detected components

Output ONLY the HTML code, nothing else.
"""
    return prompt

async def _call_claude_api(prompt: str) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise Exception("Anthropic API key not found in environment variables")

    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    data = {
        "model": "claude-3-opus-20240229",
        "max_tokens": 4000,
        "temperature": 0.7,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status != 200:
                raise Exception(f"Claude API error: {await response.text()}")
            result = await response.json()
            # Claude's response is in result['content'][0]['text']
            return result["content"][0]["text"] 