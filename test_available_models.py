"""
Test which models are available on MIMO API.
"""

import os
from dotenv import load_dotenv
import openai

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
endpoint = os.getenv("LLM_ENDPOINT")

models_to_test = [
    "deepseek-v4-flash",
    "gpt-4o",
    "gpt-4o-mini",
    "mimo-v2.5-pro"
]

print("="*80)
print("TESTING AVAILABLE MODELS ON MIMO API")
print("="*80)
print(f"\nEndpoint: {endpoint}")

working_models = []
failed_models = []

for model in models_to_test:
    print(f"\n{'='*80}")
    print(f"Testing model: {model}")
    print(f"{'='*80}")
    
    try:
        client = openai.OpenAI(api_key=api_key, base_url=endpoint)
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "Say 'Hello' in one word."}
            ],
            max_tokens=10
        )
        
        content = response.choices[0].message.content
        tokens = response.usage.total_tokens
        
        print(f"✅ SUCCESS!")
        print(f"   Response: {content}")
        print(f"   Tokens: {tokens}")
        print(f"   Model: {response.model}")
        
        working_models.append(model)
        
    except Exception as e:
        print(f"❌ FAILED")
        print(f"   Error: {str(e)[:100]}")
        failed_models.append(model)

print(f"\n{'='*80}")
print("SUMMARY")
print(f"{'='*80}")

print(f"\n✅ Working Models ({len(working_models)}):")
for model in working_models:
    print(f"   - {model}")

print(f"\n❌ Failed Models ({len(failed_models)}):")
for model in failed_models:
    print(f"   - {model}")

print(f"\n{'='*80}")