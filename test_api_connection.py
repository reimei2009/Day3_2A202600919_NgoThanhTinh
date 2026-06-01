"""
Simple test to verify API connection.
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("="*80)
print("TESTING API CONNECTION - MIMO API")
print("="*80)

# Test 1: Check environment variables
print("\n[1] Checking environment variables...")
api_key = os.getenv("OPENAI_API_KEY")
endpoint = os.getenv("LLM_ENDPOINT", "https://api.openai.com/v1")
model = os.getenv("DEFAULT_MODEL", "mimo-v2.5-pro")

print(f"✅ API Key: {api_key[:20]}... (length: {len(api_key)})")
print(f"✅ Endpoint: {endpoint}")
print(f"✅ Model: {model}")

# Test 2: Test with simple API call
print("\n[2] Testing API call...")

try:
    import openai
    
    client = openai.OpenAI(
        api_key=api_key,
        base_url=endpoint
    )
    
    print("✅ OpenAI client created")
    
    # Test with MIMO model
    print(f"\n[3] Testing with MIMO model: {model}...")
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": "Hello! Please respond with exactly: Hello World"}
        ],
        max_tokens=50
    )
    
    content = response.choices[0].message.content
    print(f"   ✅ SUCCESS! Response: {content}")
    print(f"   ✅ Model: {response.model}")
    print(f"   ✅ Tokens used: {response.usage.total_tokens}")
    
    # Save the working model
    with open("working_model.txt", "w") as f:
        f.write(model)
    print(f"\n✅ Working model saved: {model}")
    
except Exception as e:
    print(f"❌ Failed: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)