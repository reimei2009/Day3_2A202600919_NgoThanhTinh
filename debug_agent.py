"""
Debug script to test ReAct agent with detailed error logging.
"""

import sys
import os
import traceback
from dotenv import load_dotenv

load_dotenv()

print("="*80)
print("DEBUGGING REACT AGENT")
print("="*80)

# Check API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ ERROR: OPENAI_API_KEY not found in .env file")
    sys.exit(1)

print(f"✅ API Key found (length: {len(api_key)} chars)")
print(f"✅ API Key starts with: {api_key[:10]}...")

# Import agent
try:
    from src.agent.react_agent import ReActTravelAgent
    print("\n✅ ReActTravelAgent imported successfully")
except Exception as e:
    print(f"\n❌ Failed to import agent: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test with simple query
test_query = "Find me a flight from SGN to Tokyo on July 10, 2026"

print(f"\n📝 Testing query: '{test_query}'")
print("-"*80)

try:
    agent = ReActTravelAgent(max_steps=5)
    print("✅ Agent initialized")
    
    print(f"\n🔧 Agent has {len(agent.tools)} tools:")
    for tool in agent.tools:
        print(f"   - {tool['name']}")
    
    print(f"\n📋 System prompt length: {len(agent.get_system_prompt())} chars")
    
    print("\n🚀 Running agent...")
    response = agent.run(test_query)
    
    print("\n" + "="*80)
    print("✅ AGENT EXECUTION SUCCESSFUL")
    print("="*80)
    print(f"\nResponse length: {len(response)} chars")
    print(f"\nResponse:")
    print("-"*80)
    print(response)
    print("-"*80)
    
except Exception as e:
    print("\n" + "="*80)
    print("❌ AGENT EXECUTION FAILED")
    print("="*80)
    print(f"\nError: {str(e)}")
    print("\nFull traceback:")
    traceback.print_exc()
    sys.exit(1)

print("\n✅ Test completed successfully!")