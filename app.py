"""
Streamlit UI for Travel Assistant
Modern chat interface inspired by ChatGPT/Claude.
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
    page_title="Travel Assistant AI",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Modern ChatGPT/Claude style
st.markdown("""
<style>
    /* Main container */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Header styling */
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a1a;
        text-align: center;
        padding: 1.5rem 0;
        border-bottom: 2px solid #e5e5e5;
        margin-bottom: 1rem;
    }
    
    /* Chat messages */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 1rem;
    }
    
    .chat-message {
        padding: 1.2rem 1.5rem;
        border-radius: 1rem;
        margin-bottom: 1.5rem;
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* User message */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 20%;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Assistant message */
    .assistant-message {
        background-color: #f7f7f8;
        color: #1a1a1a;
        margin-right: 20%;
        border: 1px solid #e5e5e5;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    /* Pending message (typing state) */
    .pending-message {
        background-color: #f7f7f8;
        color: #666666;
        margin-right: 20%;
        border: 1px solid #e5e5e5;
        opacity: 0.6;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    /* Typing indicator */
    .typing-indicator {
        display: flex;
        gap: 4px;
        padding: 8px 12px;
    }
    
    .typing-dot {
        width: 8px;
        height: 8px;
        background-color: #666;
        border-radius: 50%;
        animation: typing 1.4s infinite ease-in-out;
    }
    
    .typing-dot:nth-child(1) { animation-delay: 0s; }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    
    @keyframes typing {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-8px); }
    }
    
    .message-role {
        font-weight: 600;
        font-size: 0.85rem;
        margin-bottom: 0.5rem;
        opacity: 0.9;
    }
    
    .message-content {
        line-height: 1.6;
    }
    
    /* Sidebar styling */
    .stSidebar {
        background-color: #f8f9fa;
        border-right: 2px solid #e5e5e5;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 0.5rem;
        font-weight: 600;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Input area */
    .input-container {
        background-color: #f7f7f8;
        padding: 1.5rem;
        border-top: 2px solid #e5e5e5;
        position: sticky;
        bottom: 0;
        z-index: 999;
    }
    
    /* Example buttons */
    .example-btn {
        background-color: #f7f7f8;
        border: 1px solid #e5e5e5;
        border-radius: 0.5rem;
        padding: 0.75rem 1rem;
        margin: 0.25rem;
        font-size: 0.9rem;
        transition: all 0.2s;
    }
    
    .example-btn:hover {
        background-color: #e8e8ea;
        transform: translateY(-1px);
    }
    
    /* Metrics */
    .metrics-container {
        background-color: #f0f0f0;
        padding: 0.75rem 1rem;
        border-radius: 0.5rem;
        margin-top: 0.5rem;
        font-size: 0.85rem;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">✈️ Travel Assistant AI</div>', unsafe_allow_html=True)

# Sidebar configuration
st.sidebar.header("⚙️ Configuration")

# Model selection with icon
st.sidebar.markdown("### 🤖 LLM Model")
model_name = st.sidebar.selectbox(
    "",
    ["mimo-v2.5-pro", "gpt-4o", "gpt-4o-mini", "deepseek-v4-flash"],
    index=0,
    label_visibility="collapsed"
)

# Agent selection
st.sidebar.markdown("### 🎭 Agent Type")
agent_type = st.sidebar.radio(
    "",
    ["ReAct Agent (with Tools)", "Chatbot Baseline (No Tools)"],
    index=0,
    label_visibility="collapsed"
)

# Max steps for ReAct agent
st.sidebar.markdown("### 🔧 Max Steps")
max_steps = st.sidebar.slider(
    "",
    min_value=3,
    max_value=15,
    value=10,
    step=1,
    label_visibility="collapsed"
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
        st.error(f"❌ Failed to initialize provider: {str(e)}")

# Initialize agent
if agent_type == "ReAct Agent (with Tools)":
    if st.session_state.agent is None or not isinstance(st.session_state.agent, ReActTravelAgent):
        try:
            st.session_state.agent = ReActTravelAgent(
                provider=st.session_state.provider,
                max_steps=max_steps
            )
        except Exception as e:
            st.error(f"❌ Failed to initialize ReAct agent: {str(e)}")
else:
    if st.session_state.agent is None or not isinstance(st.session_state.agent, ChatbotBaseline):
        try:
            st.session_state.agent = ChatbotBaseline(provider=st.session_state.provider)
        except Exception as e:
            st.error(f"❌ Failed to initialize chatbot: {str(e)}")

# Display chat history
st.markdown("### 💬 Conversation")
st.markdown("---")

chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        with st.container():
            if message["role"] == "user":
                st.markdown(f"""
                    <div class="chat-message user-message">
                        <div class="message-role">👤 You</div>
                        <div class="message-content">{message["content"]}</div>
                    </div>
                """, unsafe_allow_html=True)
            elif message["role"] == "pending":
                # Show faded message with typing indicator
                st.markdown(f"""
                    <div class="chat-message pending-message">
                        <div class="message-role">🤖 Assistant</div>
                        <div class="typing-indicator">
                            <div class="typing-dot"></div>
                            <div class="typing-dot"></div>
                            <div class="typing-dot"></div>
                        </div>
                        <div class="message-content" style="margin-top: 12px; font-style: italic;">
                            {message["content"]}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="chat-message assistant-message">
                        <div class="message-role">🤖 Assistant</div>
                        <div class="message-content">{message["content"]}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                if "metadata" in message:
                    with st.expander("📊 Details & Metrics", expanded=False):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Model", message["metadata"]["model"])
                            st.metric("Agent Type", message["metadata"]["agent_type"])
                        with col2:
                            st.metric("Total Tokens", f"{message['metadata']['total_tokens']:,}")
                            st.metric("Tool Calls", message["metadata"]["tool_calls"])
                        
                        if "events" in message["metadata"] and message["metadata"]["events"]:
                            st.markdown("**Event Counts:**")
                            st.json(message["metadata"]["events"])

# User input section - Use chat_input for better UX
st.markdown("---")

# Add clear button above input
col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    if st.button("Clear Conversation 🗑️", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
with col2:
    st.write(f"Messages: {len(st.session_state.messages)}")
with col3:
    st.write("")

# Use chat_input for Enter key support and auto-clear
user_input = st.chat_input(
    "Type your travel request here and press Enter...",
    key="chat_input"
)

# Process user input
if user_input and user_input.strip():
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Add pending message immediately (faded state)
    st.session_state.messages.append({
        "role": "pending",
        "content": "Thinking and planning your trip..."
    })
    
    # Rerun to show the pending message
    st.rerun()

# Check if there's a pending message and process it
if st.session_state.messages and st.session_state.messages[-1]["role"] == "pending":
    pending_msg = st.session_state.messages[-1]
    user_input = st.session_state.messages[-2]["content"] if len(st.session_state.messages) >= 2 else ""
    
    try:
        # Get agent response
        response = st.session_state.agent.run(user_input)
        
        # Get telemetry
        summary = logger.get_session_summary()
        
        # Replace pending message with actual response
        metadata = {
            "agent_type": agent_type,
            "model": model_name,
            "total_tokens": summary.get("total_tokens", 0),
            "tool_calls": summary.get("tool_calls", 0),
            "events": summary.get("event_counts", {})
        }
        
        st.session_state.messages[-1] = {
            "role": "assistant",
            "content": response,
            "metadata": metadata
        }
        
        # Rerun to show completed response
        st.rerun()
    
    except Exception as e:
        # Replace pending message with error
        st.session_state.messages[-1] = {
            "role": "assistant",
            "content": f"❌ Error: {str(e)}",
            "metadata": {}
        }
        st.rerun()

# Example queries section
if not st.session_state.messages:
    st.markdown("---")
    st.markdown("### 💡 Try These Examples")
    
    examples = [
        "Find me a cheap flight from SGN to Tokyo on July 10, 2026",
        "What attractions are available in Tokyo?",
        "Plan a 4-day trip to Tokyo from July 10-14, 2026 with budget of $1500",
        "Search for hotels in Hong Kong for July 10-14, 2026",
        "What's the weather forecast for Singapore on July 15, 2026?"
    ]
    
    # Example buttons in a grid
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(examples[0], use_container_width=True, key="ex1"):
            st.session_state.messages.append({"role": "user", "content": examples[0]})
            response = st.session_state.agent.run(examples[0])
            summary = logger.get_session_summary()
            metadata = {
                "agent_type": agent_type,
                "model": model_name,
                "total_tokens": summary.get("total_tokens", 0),
                "tool_calls": summary.get("tool_calls", 0),
                "events": summary.get("event_counts", {})
            }
            st.session_state.messages.append({"role": "assistant", "content": response, "metadata": metadata})
            st.rerun()
    
    with col2:
        if st.button(examples[1], use_container_width=True, key="ex2"):
            st.session_state.messages.append({"role": "user", "content": examples[1]})
            response = st.session_state.agent.run(examples[1])
            summary = logger.get_session_summary()
            metadata = {
                "agent_type": agent_type,
                "model": model_name,
                "total_tokens": summary.get("total_tokens", 0),
                "tool_calls": summary.get("tool_calls", 0),
                "events": summary.get("event_counts", {})
            }
            st.session_state.messages.append({"role": "assistant", "content": response, "metadata": metadata})
            st.rerun()
    
    with col3:
        if st.button(examples[2], use_container_width=True, key="ex3"):
            st.session_state.messages.append({"role": "user", "content": examples[2]})
            response = st.session_state.agent.run(examples[2])
            summary = logger.get_session_summary()
            metadata = {
                "agent_type": agent_type,
                "model": model_name,
                "total_tokens": summary.get("total_tokens", 0),
                "tool_calls": summary.get("tool_calls", 0),
                "events": summary.get("event_counts", {})
            }
            st.session_state.messages.append({"role": "assistant", "content": response, "metadata": metadata})
            st.rerun()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(examples[3], use_container_width=True, key="ex4"):
            st.session_state.messages.append({"role": "user", "content": examples[3]})
            response = st.session_state.agent.run(examples[3])
            summary = logger.get_session_summary()
            metadata = {
                "agent_type": agent_type,
                "model": model_name,
                "total_tokens": summary.get("total_tokens", 0),
                "tool_calls": summary.get("tool_calls", 0),
                "events": summary.get("event_counts", {})
            }
            st.session_state.messages.append({"role": "assistant", "content": response, "metadata": metadata})
            st.rerun()
    
    with col2:
        if st.button(examples[4], use_container_width=True, key="ex5"):
            st.session_state.messages.append({"role": "user", "content": examples[4]})
            response = st.session_state.agent.run(examples[4])
            summary = logger.get_session_summary()
            metadata = {
                "agent_type": agent_type,
                "model": model_name,
                "total_tokens": summary.get("total_tokens", 0),
                "tool_calls": summary.get("tool_calls", 0),
                "events": summary.get("event_counts", {})
            }
            st.session_state.messages.append({"role": "assistant", "content": response, "metadata": metadata})
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🤖 Powered by MIMO API | 🧠 ReAct Agent Architecture | ✈️ Travel Planning</p>
</div>
""", unsafe_allow_html=True)