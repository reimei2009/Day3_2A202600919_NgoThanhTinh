"""
Demo mode for testing without API key.
Uses mock responses to simulate LLM behavior.
"""

import json
import re
from typing import Dict, Any

class MockLLMProvider:
    """Mock LLM provider for demo mode."""
    
    def __init__(self, model_name: str = "mock-gpt-4o"):
        self.model_name = model_name
    
    def generate(self, prompt: str, system_prompt: str = None, 
                 temperature: float = 0.7, max_tokens: int = 1000) -> Dict[str, Any]:
        """Generate a mock response based on the prompt."""
        
        # Simulate token usage
        prompt_tokens = len(prompt.split()) * 2
        completion_tokens = 50
        total_tokens = prompt_tokens + completion_tokens
        
        # Analyze prompt to determine appropriate response
        lower_prompt = prompt.lower()
        
        # Check if this is the first step (no previous actions)
        if "previous action" not in lower_prompt and "observation" not in lower_prompt:
            # First step - analyze user query
            if "flight" in lower_prompt:
                return {
                    "content": "Thought: The user wants to find flights from SGN to Tokyo on July 10, 2026. I should use the search_flights tool to find available flights.\n\nAction: search_flights\nInput: {\"origin\": \"SGN\", \"destination\": \"NRT\", \"date\": \"2026-07-10\"}",
                    "usage": {
                        "prompt_tokens": prompt_tokens,
                        "completion_tokens": completion_tokens,
                        "total_tokens": total_tokens
                    },
                    "latency_ms": 500,
                    "model": "mock-gpt-4o"
                }
            elif "hotel" in lower_prompt:
                return {
                    "content": "Thought: The user wants to find hotels in Tokyo. I should use the search_hotels tool to find available hotels.\n\nAction: search_hotels\nInput: {\"city\": \"Tokyo\", \"check_in\": \"2026-07-10\", \"check_out\": \"2026-07-14\"}",
                    "usage": {
                        "prompt_tokens": prompt_tokens,
                        "completion_tokens": completion_tokens,
                        "total_tokens": total_tokens
                    },
                    "latency_ms": 500,
                    "model": "mock-gpt-4o"
                }
            elif "attraction" in lower_prompt:
                return {
                    "content": "Thought: The user wants to know about attractions in Tokyo. I should use the list_attractions tool.\n\nAction: list_attractions\nInput: {\"city\": \"Tokyo\"}",
                    "usage": {
                        "prompt_tokens": prompt_tokens,
                        "completion_tokens": completion_tokens,
                        "total_tokens": total_tokens
                    },
                    "latency_ms": 500,
                    "model": "mock-gpt-4o"
                }
        else:
            # Subsequent steps - provide final answer
            if "flight" in lower_prompt:
                return {
                    "content": "Thought: I have found flight information. I should now provide the final answer to the user.\n\nFinal Answer: I found 3 flights from SGN to Tokyo on July 10, 2026:\n\n1. VN Air - $420 (1 stop, 8.5 hours, 5 seats left)\n2. JAL - $680 (direct, 6 hours, 3 seats left)\n3. ANA - $720 (direct, 5.8 hours, 2 seats left)\n\nThe cheapest option is VN Air at $420.",
                    "usage": {
                        "prompt_tokens": prompt_tokens,
                        "completion_tokens": completion_tokens,
                        "total_tokens": total_tokens
                    },
                    "latency_ms": 500,
                    "model": "mock-gpt-4o"
                }
            else:
                return {
                    "content": "Final Answer: I've completed your request. Please check the tool results for detailed information.",
                    "usage": {
                        "prompt_tokens": prompt_tokens,
                        "completion_tokens": completion_tokens,
                        "total_tokens": total_tokens
                    },
                    "latency_ms": 500,
                    "model": "mock-gpt-4o"
                }
        
        # Default response
        return {
            "content": "Thought: I need to understand what the user wants and use the appropriate tool to help them.",
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens
            },
            "latency_ms": 500,
            "model": "mock-gpt-4o"
        }

if __name__ == "__main__":
    print("="*80)
    print("TESTING MOCK LLM PROVIDER")
    print("="*80)
    
    provider = MockLLMProvider()
    
    # Test 1
    print("\n[1] Testing with flight query...")
    result = provider.generate(
        "query: Find me a flight from SGN to Tokyo",
        system_prompt="You are a travel assistant."
    )
    print(f"✅ Response: {result['content'][:100]}...")
    print(f"✅ Tokens: {result['usage']['total_tokens']}")
    
    # Test 2
    print("\n[2] Testing with hotel query...")
    result = provider.generate(
        "query: Find a hotel in Tokyo",
        system_prompt="You are a travel assistant."
    )
    print(f"✅ Response: {result['content'][:100]}...")
    print(f"✅ Tokens: {result['usage']['total_tokens']}")
    
    print("\n✅ Mock provider working!")