"""
Chatbot Baseline
Simple LLM chatbot for comparison with ReAct agent.
"""

import os
from dotenv import load_dotenv
from src.core.openai_provider import OpenAIProvider
from src.telemetry.logger import logger

load_dotenv()

class ChatbotBaseline:
    """Simple baseline chatbot that uses LLM directly without tools."""
    
    def __init__(self, provider=None):
        if provider:
            self.provider = provider
        else:
            api_key = os.getenv("OPENAI_API_KEY")
            model = os.getenv("DEFAULT_MODEL", "gpt-4o")
            self.provider = OpenAIProvider(model_name=model, api_key=api_key)
    
    def run(self, user_input: str) -> str:
        """
        Process user input and return LLM response.
        
        Args:
            user_input: User's question or request
        
        Returns:
            LLM's response as a string
        """
        logger.log_event("CHATBOT_START", {"input": user_input})
        
        system_prompt = """You are a helpful travel assistant. You help users plan trips, 
find flights, hotels, and attractions. However, you do NOT have access to real-time data 
or tools. You must answer based on your general knowledge and make reasonable assumptions.

If you cannot provide specific information (like exact prices, availability, or real-time data),
be honest and tell the user you don't have access to that information.

Format your response clearly and helpfully."""
        
        try:
            response = self.provider.generate(
                prompt=user_input,
                system_prompt=system_prompt
            )
            
            result = response['content']
            logger.log_event("CHATBOT_END", {
                "output_length": len(result),
                "tokens_used": response['usage']['total_tokens'],
                "latency_ms": response['latency_ms']
            })
            
            return result
        
        except Exception as e:
            logger.error(f"Chatbot error: {str(e)}")
            return f"Sorry, I encountered an error: {str(e)}"

if __name__ == "__main__":
    # Test chatbot
    chatbot = ChatbotBaseline()
    
    test_queries = [
        "Find me a cheap flight from SGN to Tokyo in July 2026",
        "What hotels are available in Hong Kong for a 4-night stay?",
        "Plan a 5-day trip to Singapore within $2000 budget"
    ]
    
    for query in test_queries:
        print(f"\nUser: {query}")
        response = chatbot.run(query)
        print(f"Bot: {response}")
        print("-" * 80)
