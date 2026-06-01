"""
Weather Tool
Gets weather forecast for a specific city and date.
"""

import json
from datetime import datetime

def get_weather_forecast(city: str, date: str) -> dict:
    """
    Get weather forecast for a city on a specific date.
    
    Args:
        city: City name (e.g., "Tokyo", "Hong Kong")
        date: Date in YYYY-MM-DD format
    
    Returns:
        dict with 'ok' status and 'data' or 'error' information
    """
    try:
        # Load weather data
        with open('data/weather.json', 'r') as f:
            weather_data = json.load(f)
        
        # Find matching weather
        for weather in weather_data:
            if weather['city'].lower() == city.lower() and weather['date'] == date:
                return {
                    "ok": True,
                    "data": {
                        "city": weather['city'],
                        "date": weather['date'],
                        "condition": weather['condition'],
                        "temp_c_min": weather['temp_c_min'],
                        "temp_c_max": weather['temp_c_max'],
                        "is_rainy": weather['condition'] == 'rain',
                        "is_outdoor_friendly": weather['condition'] not in ['rain', 'storm']
                    }
                }
        
        return {
            "ok": False,
            "error_code": "WEATHER_NOT_FOUND",
            "message": f"Weather data not found for {city} on {date}",
            "retryable": False
        }
    
    except FileNotFoundError:
        return {
            "ok": False,
            "error_code": "DATA_NOT_FOUND",
            "message": "Weather data file not found",
            "retryable": False
        }
    except Exception as e:
        return {
            "ok": False,
            "error_code": "INTERNAL_ERROR",
            "message": f"Error getting weather forecast: {str(e)}",
            "retryable": True
        }

if __name__ == "__main__":
    # Test
    result = get_weather_forecast("Tokyo", "2026-07-10")
    print(json.dumps(result, indent=2))
