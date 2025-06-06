import openai
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_openai():
    try:
        # Initialize client
        client = openai.OpenAI(
            api_key="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"
        )
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