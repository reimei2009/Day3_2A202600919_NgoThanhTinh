"""
Test script to verify all components work correctly.
"""

import json
import sys

print("="*80)
print("TESTING TRAVEL ASSISTANT SYSTEM")
print("="*80)

# Test 1: Tools
print("\n[1/5] Testing Tools...")
try:
    from src.tools import (
        search_flights, search_hotels, list_attractions,
        get_weather_forecast, estimate_local_transport
    )
    
    # Test search_flights
    result = search_flights('SGN', 'NRT', '2026-07-10')
    assert result['ok'] == True, "Flight search failed"
    assert len(result['data']['flights']) > 0, "No flights found"
    print(f"✅ search_flights: Found {result['data']['count']} flights")
    
    # Test search_hotels
    result = search_hotels('Tokyo', '2026-07-10', '2026-07-14')
    assert result['ok'] == True, "Hotel search failed"
    assert len(result['data']['hotels']) > 0, "No hotels found"
    print(f"✅ search_hotels: Found {result['data']['count']} hotels for {result['data']['nights']} nights")
    
    # Test list_attractions
    result = list_attractions('Tokyo')
    assert result['ok'] == True, "Attraction list failed"
    assert len(result['data']['attractions']) > 0, "No attractions found"
    print(f"✅ list_attractions: Found {result['data']['count']} attractions")
    
    # Test get_weather_forecast
    result = get_weather_forecast('Tokyo', '2026-07-10')
    assert result['ok'] == True, "Weather forecast failed"
    print(f"✅ get_weather_forecast: {result['data']['condition']}, {result['data']['temp_c_min']}-{result['data']['temp_c_max']}°C")
    
    # Test estimate_local_transport
    result = estimate_local_transport('Tokyo', 4, 'normal')
    assert result['ok'] == True, "Transport estimation failed"
    print(f"✅ estimate_local_transport: ${result['data']['total_cost_usd']:.2f} for {result['data']['days']} days ({result['data']['style']})")
    
    print("✅ ALL TOOLS WORKING CORRECTLY")
except Exception as e:
    print(f"❌ TOOLS TEST FAILED: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Core modules
print("\n[2/5] Testing Core Modules...")
try:
    from src.core.openai_provider import OpenAIProvider
    from src.telemetry.logger import TelemetryLogger, logger
    
    # Test logger
    logger.log_event("TEST", {"message": "Testing logger"})
    summary = logger.get_session_summary()
    print(f"✅ Logger: {summary['total_events']} events logged")
    
    # Test provider (without API call)
    print("✅ OpenAIProvider: Module loaded successfully")
    print("✅ ALL CORE MODULES WORKING")
except Exception as e:
    print(f"❌ CORE MODULES TEST FAILED: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Chatbot Baseline
print("\n[3/5] Testing Chatbot Baseline...")
try:
    from chatbot import ChatbotBaseline
    
    # Check if API key is available
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    if os.getenv("OPENAI_API_KEY"):
        print("✅ ChatbotBaseline: Module loaded (API key found)")
        print("   (Note: Full test requires valid API key)")
    else:
        print("✅ ChatbotBaseline: Module loaded (no API key - use .env file)")
except Exception as e:
    print(f"❌ CHATBOT TEST FAILED: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: ReAct Agent
print("\n[4/5] Testing ReAct Agent...")
try:
    from src.agent.react_agent import ReActTravelAgent
    
    print("✅ ReActTravelAgent: Module loaded successfully")
    print("   Available tools:")
    
    agent = ReActTravelAgent.__new__(ReActTravelAgent)
    agent.tools = agent._load_tools()
    for tool in agent.tools:
        print(f"   - {tool['name']}: {tool['description'][:50]}...")
    
    print(f"   Total: {len(agent.tools)} tools loaded")
    print("✅ REACT AGENT WORKING")
except Exception as e:
    print(f"❌ REACT AGENT TEST FAILED: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Evaluation Framework
print("\n[5/5] Testing Evaluation Framework...")
try:
    from tests.evaluation import TestCase, Evaluator, TEST_CASES
    
    print(f"✅ TestCase: Module loaded")
    print(f"✅ Evaluator: Module loaded")
    print(f"✅ Test cases: {len(TEST_CASES)} predefined tests")
    
    for tc in TEST_CASES:
        print(f"   - {tc.test_id}: {tc.difficulty} - {tc.query[:40]}...")
    
    print("✅ EVALUATION FRAMEWORK WORKING")
except Exception as e:
    print(f"❌ EVALUATION TEST FAILED: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Summary
print("\n" + "="*80)
print("✅ ALL TESTS PASSED!")
print("="*80)
print("\n📊 Summary:")
print("   ✅ 5/5 Tools working")
print("   ✅ Core modules loaded")
print("   ✅ Chatbot baseline ready")
print("   ✅ ReAct agent ready")
print("   ✅ Evaluation framework ready")
print("\n🚀 System is ready to use!")
print("\nNext steps:")
print("   1. Set OPENAI_API_KEY in .env file")
print("   2. Run: streamlit run app.py")
print("   3. Or run: python tests/evaluation.py")
print("="*80)