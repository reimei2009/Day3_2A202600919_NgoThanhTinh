"""
Full test of ReAct agent with multiple queries.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.agent.react_agent import ReActTravelAgent
from src.telemetry.logger import logger

print("="*80)
print("FULL AGENT TEST - MIMO API")
print("="*80)

# Initialize agent
agent = ReActTravelAgent()
print(f"✅ Agent initialized with {len(agent.tools)} tools")

# Test queries
queries = [
    "Find me a flight from SGN to Tokyo on July 10, 2026",
    "Find a hotel in Tokyo from July 10-14, 2026",
    "What are the top attractions in Tokyo?",
    "What's the weather forecast for Tokyo in July 2026?"
]

for i, query in enumerate(queries, 1):
    print(f"\n{'='*80}")
    print(f"Query {i}/{len(queries)}: {query}")
    print(f"{'='*80}")
    
    try:
        response = agent.run(query)
        print(f"\n✅ Response:\n{response[:300]}...")
        print(f"\n✅ Length: {len(response)} chars")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    
    # Get session summary
    summary = logger.get_session_summary()
    print(f"\n📊 Session Stats:")
    print(f"   Total events: {summary.get('total_events', 0)}")
    print(f"   LLM calls: {summary.get('llm_calls', 0)}")
    print(f"   Tool calls: {summary.get('tool_calls', 0)}")
    print(f"   Total tokens: {summary.get('total_tokens', 0)}")

print(f"\n{'='*80}")
print("✅ ALL TESTS COMPLETED")
print(f"{'='*80}")