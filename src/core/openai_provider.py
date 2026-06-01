"""
OpenAI API Provider
Handles communication with OpenAI-compatible APIs.
"""

import os
import time
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class OpenAIProvider:
    """Provider for OpenAI-compatible LLM APIs."""
    
    def __init__(self, model_name: str = "gpt-4o", api_key: str = None, endpoint: str = None):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Model name to use
            api_key: API key (defaults to OPENAI_API_KEY env var)
            endpoint: API endpoint (defaults to OPENAI_ENDPOINT env var)
        """
        self.model_name = model_name
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.endpoint = endpoint or os.getenv("LLM_ENDPOINT", "https://api.openai.com/v1")
        
        if not self.api_key:
            raise ValueError("API key not found. Set OPENAI_API_KEY environment variable.")
    
    def generate(self, prompt: str, system_prompt: str = None, temperature: float = 0.7, max_tokens: int = 1000) -> Dict[str, Any]:
        """
        Generate text using the LLM.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
        
        Returns:
            dict with 'content', 'usage', 'latency_ms'
        """
        import openai
        
        openai.api_key = self.api_key
        openai.base_url = self.endpoint
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        start_time = time.time()
        
        try:
            response = openai.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            end_time = time.time()
            latency_ms = (end_time - start_time) * 1000
            
            return {
                "content": response.choices[0].message.content,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                "latency_ms": latency_ms,
                "model": self.model_name
            }
        
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")

if __name__ == "__main__":
    # Test
    provider = OpenAIProvider(model_name="gpt-4o")
    result = provider.generate("Say hello!")
    print(f"Response: {result['content']}")
    print(f"Tokens: {result['usage']['total_tokens']}")
    print(f"Latency: {result['latency_ms']:.2f}ms")
