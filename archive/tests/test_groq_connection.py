"""
Test Groq API Connection
========================
Test the provided Groq API key and check available models.
"""

import os
import sys
import json
from datetime import datetime

def test_groq_connection():
    """Test Groq API connection with provided key"""
    
    # Set the API key (use environment variable in production)
    api_key = "your_groq_api_key_here"
    
    try:
        # Try to import groq
        import groq
        print("✅ Groq package is installed")
        
        # Initialize client
        client = groq.Groq(api_key=api_key)
        print("✅ Groq client initialized")
        
        # Test with a simple request
        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": "Test message - respond with 'API working'"}
            ],
            model="llama3-8b-8192",
            max_tokens=10
        )
        
        content = response.choices[0].message.content
        tokens_used = response.usage.total_tokens
        
        print(f"✅ API Test Successful!")
        print(f"Response: {content}")
        print(f"Tokens used: {tokens_used}")
        
        # Get available models
        try:
            models = client.models.list()
            model_names = [model.id for model in models.data]
            print(f"✅ Available models ({len(model_names)}):")
            for model in model_names[:5]:  # Show first 5
                print(f"  - {model}")
            
            return True, {
                "api_working": True,
                "models_available": len(model_names),
                "test_response": content,
                "tokens_used": tokens_used
            }
            
        except Exception as e:
            print(f"⚠️ Could not fetch models: {e}")
            return True, {
                "api_working": True,
                "models_available": "unknown",
                "test_response": content,
                "tokens_used": tokens_used
            }
            
    except ImportError:
        print("❌ Groq package not installed")
        print("Install with: pip install groq")
        return False, {"error": "groq package not installed"}
        
    except Exception as e:
        print(f"❌ Groq API Error: {e}")
        return False, {"error": str(e)}

if __name__ == "__main__":
    success, result = test_groq_connection()
    print(f"\nTest Result: {'SUCCESS' if success else 'FAILED'}")
    print(json.dumps(result, indent=2))