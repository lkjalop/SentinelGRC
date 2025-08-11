"""
Simple Groq API Test
===================
Test without unicode characters for Windows compatibility.
"""

def test_groq_api():
    """Test Groq API with provided key"""
    
    api_key = "your_groq_api_key_here"
    
    try:
        # Try to import and use groq
        import groq
        print("SUCCESS: Groq package is installed")
        
        # Initialize client
        client = groq.Groq(api_key=api_key)
        print("SUCCESS: Groq client initialized")
        
        # Test API call
        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": "Test - respond with 'Working'"}
            ],
            model="llama3-8b-8192",
            max_tokens=5
        )
        
        content = response.choices[0].message.content
        tokens = response.usage.total_tokens
        
        print(f"SUCCESS: API Response = {content}")
        print(f"SUCCESS: Tokens used = {tokens}")
        
        return True
        
    except ImportError as e:
        print(f"ERROR: Groq package not installed - {e}")
        print("SOLUTION: pip install groq")
        return False
        
    except Exception as e:
        print(f"ERROR: API call failed - {e}")
        return False

if __name__ == "__main__":
    result = test_groq_api()
    if result:
        print("\nOVERALL: Groq API is working correctly!")
    else:
        print("\nOVERALL: Groq API setup needed")