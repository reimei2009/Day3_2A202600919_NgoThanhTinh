"""
Evaluation Framework
Compares chatbot vs ReAct agent performance on test cases.
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any
from src.core.openai_provider import OpenAIProvider
from src.agent.react_agent import ReActTravelAgent
from chatbot import ChatbotBaseline
from src.telemetry.logger import TelemetryLogger

class TestCase:
    """Represents a test case for evaluation."""
    
    def __init__(self, test_id: str, query: str, 
                 expected_tools: List[str] = None,
                 expected_keywords: List[str] = None,
                 difficulty: str = "medium"):
        self.test_id = test_id
        self.query = query
        self.expected_tools = expected_tools or []
        self.expected_keywords = expected_keywords or []
        self.difficulty = difficulty

class Evaluator:
    """Evaluates agent performance."""
    
    def __init__(self, model_name: str = "gpt-4o"):
        self.model_name = model_name
        self.provider = OpenAIProvider(model_name=model_name)
        self.logger = TelemetryLogger(log_dir="logs/eval")
    
    def run_test_case(self, test_case: TestCase, agent, agent_type: str) -> Dict[str, Any]:
        self.logger.log_event("TEST_START", {
            "test_id": test_case.test_id,
            "agent_type": agent_type,
            "query": test_case.query
        })
        
        start_time = time.time()
        
        try:
            response = agent.run(test_case.query)
            elapsed_time = time.time() - start_time
            summary = self.logger.get_session_summary()
            
            result = {
                "test_id": test_case.test_id,
                "agent_type": agent_type,
                "query": test_case.query,
                "response": response,
                "response_length": len(response),
                "elapsed_time_s": elapsed_time,
                "tokens_used": summary["total_tokens"],
                "tool_calls": summary["tool_calls"],
                "success": True,
                "error": None
            }
            
            if test_case.expected_keywords:
                found_keywords = [
                    kw for kw in test_case.expected_keywords 
                    if kw.lower() in response.lower()
                ]
                result["expected_keywords_found"] = found_keywords
                result["keyword_coverage"] = len(found_keywords) / len(test_case.expected_keywords)
            
            if agent_type == "react" and test_case.expected_tools:
                tools_called = [e["data"]["tool"] for e in self.logger.session_data["events"] 
                              if e["event_type"] == "TOOL_CALL"]
                result["tools_called"] = list(set(tools_called))
                result["expected_tools_called"] = [t for t in test_case.expected_tools if t in tools_called]
                result["tool_coverage"] = len(result["expected_tools_called"]) / len(test_case.expected_tools)
            
            self.logger.log_event("TEST_COMPLETE", {
                "test_id": test_case.test_id,
                "agent_type": agent_type,
                "success": True,
                "elapsed_time": elapsed_time
            })
            
            return result
        
        except Exception as e:
            elapsed_time = time.time() - start_time
            
            self.logger.log_event("TEST_FAILED", {
                "test_id": test_case.test_id,
                "agent_type": agent_type,
                "error": str(e)
            })
            
            return {
                "test_id": test_case.test_id,
                "agent_type": agent_type,
                "query": test_case.query,
                "response": None,
                "elapsed_time_s": elapsed_time,
                "tokens_used": 0,
                "tool_calls": 0,
                "success": False,
                "error": str(e)
            }
    
    def evaluate(self, test_cases: List[TestCase]) -> Dict[str, Any]:
        results = {
            "timestamp": datetime.now().isoformat(),
            "model": self.model_name,
            "test_cases": [],
            "summary": {}
        }
        
        for test_case in test_cases:
            chatbot = ChatbotBaseline(provider=self.provider)
            chatbot_result = self.run_test_case(test_case, chatbot, "chatbot")
            
            react_agent = ReActTravelAgent(provider=self.provider, max_steps=10)
            react_result = self.run_test_case(test_case, react_agent, "react")
            
            results["test_cases"].append({
                "test_case": {
                    "id": test_case.test_id,
                    "query": test_case.query,
                    "difficulty": test_case.difficulty
                },
                "chatbot": chatbot_result,
                "react": react_result
            })
        
        chatbot_results = [tc["chatbot"] for tc in results["test_cases"]]
        react_results = [tc["react"] for tc in results["test_cases"]]
        
        results["summary"] = {
            "chatbot": {
                "total_tests": len(chatbot_results),
                "successful": sum(1 for r in chatbot_results if r["success"]),
                "avg_response_time": sum(r["elapsed_time_s"] for r in chatbot_results) / len(chatbot_results),
                "avg_tokens": sum(r["tokens_used"] for r in chatbot_results) / len(chatbot_results),
                "avg_response_length": sum(r["response_length"] for r in chatbot_results) / len(chatbot_results)
            },
            "react": {
                "total_tests": len(react_results),
                "successful": sum(1 for r in react_results if r["success"]),
                "avg_response_time": sum(r["elapsed_time_s"] for r in react_results) / len(react_results),
                "avg_tokens": sum(r["tokens_used"] for r in react_results) / len(react_results),
                "avg_response_length": sum(r["response_length"] for r in react_results) / len(react_results),
                "avg_tool_calls": sum(r["tool_calls"] for r in react_results) / len(react_results)
            }
        }
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"logs/eval/results_{timestamp}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        results["results_file"] = results_file
        
        return results

TEST_CASES = [
    TestCase(
        test_id="TC-001",
        query="Find me a cheap flight from SGN to Tokyo on July 10, 2026",
        expected_tools=["search_flights"],
        expected_keywords=["flight", "Tokyo", "price"],
        difficulty="easy"
    ),
    TestCase(
        test_id="TC-002",
        query="What attractions are available in Tokyo?",
        expected_tools=["list_attractions"],
        expected_keywords=["attraction", "Tokyo", "museum"],
        difficulty="easy"
    ),
    TestCase(
        test_id="TC-003",
        query="Plan a 4-day trip to Tokyo from July 10-14, 2026 with budget of $1500",
        expected_tools=["search_flights", "search_hotels", "list_attractions", "build_itinerary"],
        expected_keywords=["flight", "hotel", "attraction", "budget"],
        difficulty="hard"
    ),
    TestCase(
        test_id="TC-004",
        query="Search for budget hotels in Hong Kong for July 10-14, 2026",
        expected_tools=["search_hotels"],
        expected_keywords=["hotel", "Hong Kong", "budget"],
        difficulty="medium"
    ),
    TestCase(
        test_id="TC-005",
        query="What's the weather forecast for Singapore on July 15, 2026?",
        expected_tools=["get_weather_forecast"],
        expected_keywords=["weather", "Singapore", "forecast"],
        difficulty="easy"
    )
]

if __name__ == "__main__":
    print("Running evaluation...")
    evaluator = Evaluator(model_name="gpt-4o")
    results = evaluator.evaluate(TEST_CASES)
    
    print(f"\nEvaluation complete!")
    print(f"Results saved to: {results['results_file']}")
    print(f"\nSummary:")
    print(f"Chatbot: {results['summary']['chatbot']['successful']}/{results['summary']['chatbot']['total_tests']} successful")
    print(f"ReAct: {results['summary']['react']['successful']}/{results['summary']['react']['total_tests']} successful")
    print(f"\nAverage response time:")
    print(f"Chatbot: {results['summary']['chatbot']['avg_response_time']:.2f}s")
    print(f"ReAct: {results['summary']['react']['avg_response_time']:.2f}s")