import os
import pytest
from langchain_openai import OpenAI
from openai import AuthenticationError

def test_openai_connection():
    """Test if OpenAI API key is valid and can establish a connection"""
    api_key = os.getenv("OPENAI_API_KEY")
    
    # Check if API key exists
    if not api_key:
        pytest.skip("OPENAI_API_KEY not found in environment variables")
    
    try:
        # Initialize OpenAI client
        llm = OpenAI(api_key=api_key)
        
        # Make a simple API call to test connection
        print("\n=== Starting OpenAI API Call ===")
        response = llm.invoke("Say 'test' if you can read this.")
        print("\n=== OpenAI Response ===")
        print(f"Raw response: {repr(response)}")
        print(f"Response type: {type(response)}")
        print(f"Response length: {len(response)}")
        print("=== End Response ===\n")
        
        # Check if we got a response
        assert response is not None
        assert isinstance(response, str)
        assert len(response) > 0
        
    except AuthenticationError:
        pytest.fail("OpenAI API key is invalid")
    except Exception as e:
        pytest.fail(f"Failed to connect to OpenAI: {str(e)}") 