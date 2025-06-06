import os
import openai
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_openai():
    try:
        # Initialize client
        client = openai.OpenAI(api_key=api_key)
        logger.info("OpenAI client initialized successfully")
        
        # Test a simple API call
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello!"}
            ],
            max_tokens=10
        )
        logger.info("API call successful")
        logger.info(f"Response: {response.choices[0].message.content}")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    test_openai() 