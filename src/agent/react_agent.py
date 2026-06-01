"""
ReAct Agent Implementation
Thought-Action-Observation loop for travel planning.
"""

import os
import re
import json
from dotenv import load_dotenv
from src.core.openai_provider import OpenAIProvider
from src.telemetry.logger import logger
from typing import Dict, Any

load_dotenv()

class ReActTravelAgent:
    """
    ReAct-style Agent that follows the Thought-Action-Observation loop.
    """
    
    def __init__(self, provider=None, max_steps: int = 10):
        if provider:
            self.provider = provider
        else:
            api_key = os.getenv("OPENAI_API_KEY")
            model = os.getenv("DEFAULT_MODEL", "gpt-4o")
            self.provider = OpenAIProvider(model_name=model, api_key=api_key)
        
        self.max_steps = max_steps
        self.tools = self._load_tools()
    
    def _load_tools(self) -> list:
        """Load available tools."""
        from src.tools import (
            search_flights, search_hotels, list_attractions,
            get_weather_forecast, estimate_local_transport,
            build_itinerary, estimate_trip_total
        )
        
        return [
            {
                "name": "search_flights",
                "description": "Search for available flights. Args: origin (airport code like SGN/HAN), destination (airport code like NRT/HKG/BKK/SIN), depart_date (YYYY-MM-DD), budget_max (optional, in USD)",
                "function": search_flights
            },
            {
                "name": "search_hotels",
                "description": "Search for available hotels. Args: city (city name), check_in (YYYY-MM-DD), check_out (YYYY-MM-DD), budget_max (optional, per night USD), min_rating (optional)",
                "function": search_hotels
            },
            {
                "name": "list_attractions",
                "description": "List attractions in a city. Args: city (city name), tags (optional list like ['museum', 'indoor']), budget_max (optional, ticket price USD)",
                "function": list_attractions
            },
            {
                "name": "get_weather_forecast",
                "description": "Get weather forecast for a city and date. Args: city (city name), date (YYYY-MM-DD)",
                "function": get_weather_forecast
            },
            {
                "name": "estimate_local_transport",
                "description": "Estimate local transport costs. Args: city (city name), days (number of days), style (budget/normal/comfort)",
                "function": estimate_local_transport
            },
            {
                "name": "build_itinerary",
                "description": "Build complete itinerary. Args: flight_ids (list of flight IDs), hotel_id (hotel ID), attraction_ids (list of attraction IDs), check_in (YYYY-MM-DD), check_out (YYYY-MM-DD), budget_limit (optional)",
                "function": build_itinerary
            },
            {
                "name": "estimate_trip_total",
                "description": "Estimate total trip cost including all components. Args: flight_ids (list), hotel_id, attraction_ids (list), check_in, check_out, transport_style (budget/normal/comfort)",
                "function": estimate_trip_total
            }
        ]
    
    def get_system_prompt(self) -> str:
        """Generate system prompt with tool descriptions."""
        tool_descriptions = "\n".join([
            f"- {tool['name']}: {tool['description']}"
            for tool in self.tools
        ])
        
        return f"""You are an intelligent travel planning assistant. You have access to the following tools to help plan trips:

{tool_descriptions}

IMPORTANT INSTRUCTIONS:
1. Follow this exact format for each step:
   Thought: [your reasoning about what to do next]
   Action: tool_name(arg1="value1", arg2="value2")
   Observation: [result will be provided here]

2. After calling a tool and receiving the Observation, continue with your next Thought.

3. Once you have gathered all necessary information and can provide a complete answer, use:
   Final Answer: [your comprehensive response to the user]

4. Tool arguments must be in Python function call format with double quotes for strings.

5. Always check tool results for errors. If a tool fails, explain why and try an alternative approach.

6. Be thorough - gather all relevant information (flights, hotels, attractions, weather) before providing final answer.

7. Always consider budget constraints mentioned by the user.

8. When checking dates, use the current date: 2026-06-01"""

    def _parse_action(self, action_text: str) -> tuple:
        """Parse action text to extract tool name and arguments."""
        # Match: tool_name(arg1="value1", arg2="value2")
        match = re.match(r'(\w+)\s*\((.*)\)', action_text.strip())
        if not match:
            return None, None
        
        tool_name = match.group(1)
        args_str = match.group(2)
        
        # Parse arguments
        args = {}
        if args_str.strip():
            # Parse key-value pairs
            for pair in args_str.split(','):
                pair = pair.strip()
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Handle quotes
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
                    # Handle lists
                    elif value.startswith('[') and value.endswith(']'):
                        value = eval(value)
                    # Handle numbers
                    elif value.replace('.', '').isdigit():
                        value = float(value) if '.' in value else int(value)
                    
                    args[key] = value
        
        return tool_name, args
    
    def _execute_tool(self, tool_name: str, args: dict) -> str:
        """Execute a tool with given arguments."""
        logger.log_event("TOOL_CALL", {"tool": tool_name, "args": args})
        
        tool = next((t for t in self.tools if t['name'] == tool_name), None)
        if not tool:
            error_msg = f"Tool '{tool_name}' not found"
            logger.error(error_msg)
            return f"Error: {error_msg}"
        
        try:
            result = tool['function'](**args)
            
            if result['ok']:
                # Format successful result
                if 'data' in result:
                    return json.dumps(result['data'], indent=2, ensure_ascii=False)
                else:
                    return "Success: " + str(result)
            else:
                # Return error information
                error_msg = f"Error ({result.get('error_code', 'UNKNOWN')}): {result.get('message', 'Unknown error')}"
                if result.get('retryable'):
                    error_msg += " (retryable)"
                return error_msg
        
        except Exception as e:
            error_msg = f"Error executing tool: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def run(self, user_input: str) -> str:
        """
        Run the ReAct agent on user input.
        
        Args:
            user_input: User's travel planning request
        
        Returns:
            Final answer or error message
        """
        logger.log_event("AGENT_START", {
            "input": user_input,
            "model": self.provider.model_name,
            "max_steps": self.max_steps
        })
        
        conversation = []
        conversation.append(f"User: {user_input}")
        
        steps = 0
        current_prompt = user_input
        
        while steps < self.max_steps:
            # Generate LLM response
            try:
                response = self.provider.generate(
                    prompt=current_prompt,
                    system_prompt=self.get_system_prompt()
                )
                
                llm_output = response['content']
                logger.log_event("LLM_RESPONSE", {
                    "step": steps + 1,
                    "tokens": response['usage']['total_tokens'],
                    "latency_ms": response['latency_ms']
                })
            except Exception as e:
                logger.error(f"LLM generation error: {str(e)}")
                return f"Error: Failed to generate response - {str(e)}"
            
            # Parse the response
            lines = llm_output.split('\n')
            thought = None
            action = None
            observation = None
            final_answer = None
            
            for i, line in enumerate(lines):
                if line.startswith("Thought:"):
                    thought = line[8:].strip()
                elif line.startswith("Action:"):
                    action = line[7:].strip()
                elif line.startswith("Final Answer:"):
                    final_answer = '\n'.join(lines[i:])[13:].strip()
                    break
            
            # Check for Final Answer
            if final_answer:
                logger.log_event("AGENT_SUCCESS", {
                    "steps": steps + 1,
                    "output_length": len(final_answer)
                })
                return final_answer
            
            # Check for Action
            if not action:
                logger.log_event("AGENT_ERROR", {
                    "reason": "No action found in LLM output",
                    "output": llm_output
                })
                return f"Error: Agent failed to generate action. Output: {llm_output}"
            
            # Execute action
            tool_name, args = self._parse_action(action)
            if not tool_name:
                logger.log_event("AGENT_ERROR", {
                    "reason": "Failed to parse action",
                    "action": action
                })
                return f"Error: Failed to parse action: {action}"
            
            observation = self._execute_tool(tool_name, args)
            
            # Build conversation for next iteration
            conversation.append(f"Thought: {thought}")
            conversation.append(f"Action: {action}")
            conversation.append(f"Observation: {observation}")
            
            current_prompt = "\n".join(conversation)
            
            steps += 1
        
        # Max steps reached
        logger.log_event("AGENT_TIMEOUT", {"steps": steps})
        return f"Error: Agent reached maximum steps ({self.max_steps}) without providing a final answer. Last observation: {observation}"

if __name__ == "__main__":
    # Test ReAct agent
    agent = ReActTravelAgent(max_steps=10)
    
    test_queries = [
        "Find me a cheap flight from SGN to Tokyo on July 10, 2026",
        "What attractions are available in Tokyo?",
        "Plan a 4-day trip to Tokyo from July 10-14, 2026 with budget of $1500"
    ]
    
    for query in test_queries:
        print(f"\n{'='*80}")
        print(f"User: {query}")
        print(f"{'='*80}")
        response = agent.run(query)
        print(f"\nAgent: {response}")
