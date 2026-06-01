import os

# Create Streamlit UI
streamlit_ui = '''"""
Streamlit UI for Travel Assistant
Interactive interface for comparing chatbot vs ReAct agent.
"""

import streamlit as st
import os
from dotenv import load_dotenv
from src.core.openai_provider import OpenAIProvider
from src.agent.react_agent import ReActTravelAgent
from chatbot import ChatbotBaseline
from src.telemetry.logger import logger

load_dotenv()

# Page config
st.set_page_config(
    page_title="Travel Assistant - Chatbot vs ReAct Agent",
    page_icon="✈️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #1f77b4;
    }
    .bot-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
    }
    .success {
        color: #2e7d32;
        font-weight: bold;
    }
    .error {
        color: #c62828;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">✈️ Travel Assistant: Chatbot vs ReAct Agent</div>', unsafe_allow_html=True)

st.markdown("""
This application demonstrates the difference between a simple chatbot and a ReAct (Reasoning + Acting) agent 
for travel planning tasks. Both use the same underlying LLM, but the ReAct agent has access to tools and follows 
a structured reasoning process.
""")

# Sidebar configuration
st.sidebar.header("⚙️ Configuration")

# Agent selection
agent_type = st.sidebar.radio(
    "Select Agent Type",
    ["ReAct Agent (with Tools)", "Chatbot Baseline (No Tools)"],
    index=0
)

# Model selection
model_name = st.sidebar.selectbox(
    "LLM Model",
    ["gpt-4o", "gpt-4o-mini", "deepseek-v4-flash"],
    index=0
)

# Max steps for ReAct agent
max_steps = st.sidebar.slider(
    "Max Steps (ReAct Agent)",
    min_value=3,
    max_value=15,
    value=10,
    step=1
)

# Temperature
temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.1
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'agent' not in st.session_state:
    st.session_state.agent = None
if 'provider' not in st.session_state:
    st.session_state.provider = None

# Initialize agent/provider if needed
if st.session_state.provider is None or st.session_state.provider.model_name != model_name:
    try:
        st.session_state.provider = OpenAIProvider(model_name=model_name)
        st.session_state.agent = None
    except Exception as e:
        st.error(f"Failed to initialize provider: {str(e)}")

# Initialize agent
if agent_type == "ReAct Agent (with Tools)":
    if st.session_state.agent is None or not isinstance(st.session_state.agent, ReActTravelAgent):
        try:
            st.session_state.agent = ReActTravelAgent(
                provider=st.session_state.provider,
                max_steps=max_steps
            )
        except Exception as e:
            st.error(f"Failed to initialize ReAct agent: {str(e)}")
else:
    if st.session_state.agent is None or not isinstance(st.session_state.agent, ChatbotBaseline):
        try:
            st.session_state.agent = ChatbotBaseline(provider=st.session_state.provider)
        except Exception as e:
            st.error(f"Failed to initialize chatbot: {str(e)}")

# Display chat history
st.subheader("💬 Conversation")

for message in st.session_state.messages:
    with st.container():
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user-message"><strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message bot-message"><strong>Agent:</strong></div>', unsafe_allow_html=True)
            st.markdown(message["content"])
            if "metadata" in message:
                with st.expander("📊 Details"):
                    st.json(message["metadata"])

# User input
user_input = st.text_area(
    "Your travel request:",
    height=100,
    placeholder="e.g., 'Find me a cheap flight from SGN to Tokyo on July 10, 2026 with budget of $1500 for 4 days'"
)

col1, col2 = st.columns([1, 5])

with col1:
    send_button = st.button("Send", type="primary", use_container_width=True)

with col2:
    clear_button = st.button("Clear Conversation", use_container_width=True)

# Clear button
if clear_button:
    st.session_state.messages = []
    st.rerun()

# Send button
if send_button and user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get agent response
    with st.spinner("Processing your request..."):
        try:
            response = st.session_state.agent.run(user_input)
            
            # Get telemetry
            summary = logger.get_session_summary()
            
            # Add agent response
            metadata = {
                "agent_type": agent_type,
                "model": model_name,
                "total_tokens": summary["total_tokens"],
                "tool_calls": summary["tool_calls"],
                "events": summary["event_counts"]
            }
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "metadata": metadata
            })
            
            st.rerun()
        
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Example queries
st.divider()
st.subheader("📝 Example Queries")

examples = [
    "Find me a cheap flight from SGN to Tokyo on July 10, 2026",
    "What attractions are available in Tokyo?",
    "Plan a 4-day trip to Tokyo from July 10-14, 2026 with budget of $1500",
    "Search for hotels in Hong Kong for July 10-14, 2026",
    "What's the weather forecast for Singapore on July 15, 2026?"
]

col1, col2, col3 = st.columns(3)

with col1:
    if st.button(examples[0], use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": examples[0]})
        try:
            response = st.session_state.agent.run(examples[0])
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")

with col2:
    if st.button(examples[1], use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": examples[1]})
        try:
            response = st.session_state.agent.run(examples[1])
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")

with col3:
    if st.button(examples[2], use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": examples[2]})
        try:
            response = st.session_state.agent.run(examples[2])
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")

col1, col2 = st.columns(2)

with col1:
    if st.button(examples[3], use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": examples[3]})
        try:
            response = st.session_state.agent.run(examples[3])
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")

with col2:
    if st.button(examples[4], use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": examples[4]})
        try:
            response = st.session_state.agent.run(examples[4])
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")
'''

# Create Evaluation Framework
eval_framework = '''"""
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
        """
        Initialize test case.
        
        Args:
            test_id: Unique identifier
            query: User query
            expected_tools: List of tools that should be called
            expected_keywords: Keywords that should appear in response
            difficulty: easy/medium/hard
        """
        self.test_id = test_id
        self.query = query
        self.expected_tools = expected_tools or []
        self.expected_keywords = expected_keywords or []
        self.difficulty = difficulty

class Evaluator:
    """Evaluates agent performance."""
    
    def __init__(self, model_name: str = "gpt-4o"):
        """
        Initialize evaluator.
        
        Args:
            model_name: LLM model to use
        """
        self.model_name = model_name
        self.provider = OpenAIProvider(model_name=model_name)
        self.logger = TelemetryLogger(log_dir="logs/eval")
    
    def run_test_case(self, test_case: TestCase, agent, agent_type: str) -> Dict[str, Any]:
        """
        Run a single test case.
        
        Args:
            test_case: Test case to run
            agent: Agent instance
            agent_type: "chatbot" or "react"
        
        Returns:
            Test result dictionary
        """
        self.logger.log_event("TEST_START", {
            "test_id": test_case.test_id,
            "agent_type": agent_type,
            "query": test_case.query
        })
        
        start_time = time.time()
        
        try:
            # Run agent
            response = agent.run(test_case.query)
            
            elapsed_time = time.time() - start_time
            
            # Get telemetry
            summary = self.logger.get_session_summary()
            
            # Evaluate response
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
            
            # Check for expected keywords
            if test_case.expected_keywords:
                found_keywords = [
                    kw for kw in test_case.expected_keywords 
                    if kw.lower() in response.lower()
                ]
                result["expected_keywords_found"] = found_keywords
                result["keyword_coverage"] = len(found_keywords) / len(test_case.expected_keywords)
            
            # Check for expected tools (only for ReAct)
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
        """
        Evaluate both agents on all test cases.
        
        Args:
            test_cases: List of test cases
        
        Returns:
            Evaluation results
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "model": self.model_name,
            "test_cases": [],
            "summary": {}
        }
        
        for test_case in test_cases:
            # Test chatbot
            chatbot = ChatbotBaseline(provider=self.provider)
            chatbot_result = self.run_test_case(test_case, chatbot, "chatbot")
            
            # Test ReAct agent
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
        
        # Calculate summary statistics
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
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"logs/eval/results_{timestamp}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        results["results_file"] = results_file
        
        return results

# Predefined test cases
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
    
    print(f"\\nEvaluation complete!")
    print(f"Results saved to: {results['results_file']}")
    print(f"\\nSummary:")
    print(f"Chatbot: {results['summary']['chatbot']['successful']}/{results['summary']['chatbot']['total_tests']} successful")
    print(f"ReAct: {results['summary']['react']['successful']}/{results['summary']['react']['total_tests']} successful")
    print(f"\\nAverage response time:")
    print(f"Chatbot: {results['summary']['chatbot']['avg_response_time']:.2f}s")
    print(f"ReAct: {results['summary']['react']['avg_response_time']:.2f}s")
'''

# Write files
with open('app.py', 'w') as f:
    f.write(streamlit_ui)
print("✅ Created app.py (Streamlit UI)")

with open('tests/evaluation.py', 'w') as f:
    f.write(eval_framework)
print("✅ Created tests/evaluation.py")

print("\\n🎉 UI and Evaluation framework created successfully!")
print("\\nTo run the UI: streamlit run app.py")
print("To run evaluation: python tests/evaluation.py")