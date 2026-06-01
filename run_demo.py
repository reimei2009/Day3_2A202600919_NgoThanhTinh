"""
Run the ReAct agent with demo mode (mock LLM).
This allows testing without API key.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.agent.react_agent import ReActTravelAgent
from src.telemetry.logger import TelemetryLogger, logger
from demo_mode import MockLLMProvider

print("="*80)
print("REACT AGENT - DEMO MODE")
print("="*80)

# Create mock provider
mock_provider = MockLLMProvider()

# Patch the ReAct agent to use mock provider
agent = ReActTravelAgent.__new__(ReActTravelAgent)
agent.provider = mock_provider
agent.model_name = "mock-gpt-4o"
agent.max_steps = 10
agent.logger = logger
agent.tools = agent._load_tools()

print(f"\n✅ Agent initialized with {len(agent.tools)} tools")
print("✅ Using mock LLM provider (no API key needed)")

# Test query
test_query = "Find me a flight from SGN to Tokyo on July 10, 2026"

print(f"\n📝 Testing query: '{test_query}'")
print("-"*80)

# Run agent
try:
    response = agent.run(test_query)
    
    print("\n" + "="*80)
    print("✅ AGENT EXECUTION SUCCESSFUL")
    print("="*80)
    print(f"\nResponse:")
    print("-"*80)
    print(response)
    print("-"*80)
    
    # Show telemetry
    summary = logger.get_session_summary()
    print(f"\n📊 Telemetry:")
    print(f"   Total events: {summary.get('total_events', 0)}")
    print(f"   LLM calls: {summary.get('llm_calls', 0)}")
    print(f"   Tool calls: {summary.get('tool_calls', 0)}")
    print(f"   Total tokens: {summary.get('total_tokens', 0)}")
    
except Exception as e:
    print("\n" + "="*80)
    print("❌ AGENT EXECUTION FAILED")
    print("="*80)
    print(f"\nError: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n✅ Demo mode working!")
print("\n💡 To use with real LLM:")
print("   1. Fix API key in .env file")
print("   2. Run: python debug_agent.py")
print("="*80)