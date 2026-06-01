"""
Attractions Tool
Lists attractions in a city with filtering options.
"""

import json
from datetime import datetime

def list_attractions(city: str, tags: list = None, budget_max: float = None) -> dict:
    """
    List attractions in a city with optional filtering.
    
    Args:
        city: City name (e.g., "Tokyo", "Hong Kong")
        tags: List of tags to filter (e.g., ["museum", "indoor"])
        budget_max: Maximum ticket price in USD (optional)
    
    Returns:
        dict with 'ok' status and 'data' or 'error' information
    """
    try:
        # Load attractions data
        with open('data/attractions.json', 'r') as f:
            attractions = json.load(f)
        
        # Filter attractions
        matching_attractions = []
        for attraction in attractions:
            if attraction['city'].lower() == city.lower():
                # Check tags if provided
                if tags:
                    if not any(tag in attraction['tags'] for tag in tags):
                        continue
                
                # Check budget if provided
                if budget_max and attraction['ticket_price_usd'] > budget_max:
                    continue
                
                matching_attractions.append(attraction)
        
        if not matching_attractions:
            return {
                "ok": False,
                "error_code": "NO_ATTRACTION_FOUND",
                "message": f"No attractions found in {city} matching criteria",
                "retryable": False
            }
        
        # Sort by rating (using ticket price as proxy for popularity)
        matching_attractions.sort(key=lambda x: -x['ticket_price_usd'])
        
        return {
            "ok": True,
            "data": {
                "attractions": matching_attractions[:10],
                "count": len(matching_attractions)
            }
        }
    
    except FileNotFoundError:
        return {
            "ok": False,
            "error_code": "DATA_NOT_FOUND",
            "message": "Attractions data file not found",
            "retryable": False
        }
    except Exception as e:
        return {
            "ok": False,
            "error_code": "INTERNAL_ERROR",
            "message": f"Error listing attractions: {str(e)}",
            "retryable": True
        }

if __name__ == "__main__":
    # Test
    result = list_attractions("Tokyo", ["museum"])
    print(json.dumps(result, indent=2))
