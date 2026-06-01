"""
Transport Cost Estimation Tool
Estimates local transportation costs based on city and travel style.
"""

import json

def estimate_local_transport(city: str, days: int, style: str = "normal") -> dict:
    """
    Estimate local transportation costs for a trip.
    
    Args:
        city: City name (e.g., "Tokyo", "Hong Kong")
        days: Number of days
        style: Travel style - "budget", "normal", or "comfort"
    
    Returns:
        dict with 'ok' status and 'data' or 'error' information
    """
    try:
        # Load transport rules
        with open('data/transport_rules.json', 'r') as f:
            transport_rules = json.load(f)
        
        # Find city
        city_key = None
        for key in transport_rules.keys():
            if key.lower() == city.lower():
                city_key = key
                break
        
        if not city_key:
            return {
                "ok": False,
                "error_code": "CITY_NOT_FOUND",
                "message": f"Transport rules not found for city: {city}",
                "retryable": False
            }
        
        # Get daily cost
        if style not in transport_rules[city_key]:
            style = "normal"  # Default to normal
        
        daily_cost = transport_rules[city_key][style]["daily_usd"]
        total_cost = daily_cost * days
        
        return {
            "ok": True,
            "data": {
                "city": city_key,
                "days": days,
                "style": style,
                "daily_cost_usd": daily_cost,
                "total_cost_usd": total_cost
            }
        }
    
    except FileNotFoundError:
        return {
            "ok": False,
            "error_code": "DATA_NOT_FOUND",
            "message": "Transport rules data file not found",
            "retryable": False
        }
    except Exception as e:
        return {
            "ok": False,
            "error_code": "INTERNAL_ERROR",
            "message": f"Error estimating transport costs: {str(e)}",
            "retryable": True
        }

if __name__ == "__main__":
    # Test
    result = estimate_local_transport("Tokyo", 4, "normal")
    print(json.dumps(result, indent=2))
