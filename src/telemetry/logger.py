"""
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
            f.write(json.dumps(event) + "\n")
    
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
