import os

# Create OpenAI Provider
openai_provider_code = '''"""
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
'''

# Create Logger
logger_code = '''"""
Telemetry Logger
Logs agent events for analysis and debugging.
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, Any

class TelemetryLogger:
    """Logger for tracking agent events."""
    
    def __init__(self, log_dir: str = "logs"):
        """
        Initialize logger.
        
        Args:
            log_dir: Directory to store log files
        """
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
        # Create session log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(log_dir, f"session_{timestamp}.log")
        
        # Initialize session data
        self.session_data = {
            "session_start": datetime.now().isoformat(),
            "events": []
        }
    
    def log_event(self, event_type: str, data: Dict[str, Any] = None):
        """
        Log an event.
        
        Args:
            event_type: Type of event (e.g., "AGENT_START", "TOOL_CALL")
            data: Event data as dictionary
        """
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "data": data or {}
        }
        
        self.session_data["events"].append(event)
        
        # Append to log file
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(event) + "\\n")
    
    def error(self, message: str):
        """Log an error message."""
        self.log_event("ERROR", {"message": message})
        print(f"[ERROR] {message}")
    
    def get_session_summary(self) -> Dict[str, Any]:
        """
        Get summary of the current session.
        
        Returns:
            Session statistics
        """
        events = self.session_data["events"]
        
        # Count event types
        event_counts = {}
        for event in events:
            etype = event["event_type"]
            event_counts[etype] = event_counts.get(etype, 0) + 1
        
        # Calculate token usage
        total_tokens = 0
        for event in events:
            if "tokens" in event.get("data", {}):
                total_tokens += event["data"]["tokens"]
        
        # Count tool calls
        tool_calls = [e for e in events if e["event_type"] == "TOOL_CALL"]
        
        return {
            "session_start": self.session_data["session_start"],
            "total_events": len(events),
            "event_counts": event_counts,
            "total_tokens": total_tokens,
            "tool_calls": len(tool_calls),
            "log_file": self.log_file
        }
    
    def save_session(self):
        """Save complete session data to JSON file."""
        summary_file = self.log_file.replace(".log", "_summary.json")
        with open(summary_file, 'w') as f:
            json.dump(self.session_data, f, indent=2)
        
        return summary_file

# Global logger instance
logger = TelemetryLogger()

if __name__ == "__main__":
    # Test logger
    logger.log_event("TEST_EVENT", {"message": "Testing logger"})
    logger.error("Test error message")
    
    summary = logger.get_session_summary()
    print(f"Session Summary: {json.dumps(summary, indent=2)}")
'''

# Write core module files
with open('src/core/__init__.py', 'w') as f:
    f.write('"""Core modules for the travel assistant."""\nfrom .openai_provider import OpenAIProvider\n\n__all__ = ["OpenAIProvider"]\n')
print("✅ Created src/core/__init__.py")

with open('src/core/openai_provider.py', 'w') as f:
    f.write(openai_provider_code)
print("✅ Created src/core/openai_provider.py")

with open('src/telemetry/__init__.py', 'w') as f:
    f.write('"""Telemetry and logging modules."""\nfrom .logger import TelemetryLogger, logger\n\n__all__ = ["TelemetryLogger", "logger"]\n')
print("✅ Created src/telemetry/__init__.py")

with open('src/telemetry/logger.py', 'w') as f:
    f.write(logger_code)
print("✅ Created src/telemetry/logger.py")

print("\n🎉 Core modules created successfully!")