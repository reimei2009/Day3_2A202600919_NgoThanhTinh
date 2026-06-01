"""
Hotel Search Tool
Searches for available hotels in a specific city.
"""

import json
from datetime import datetime

def search_hotels(city: str, check_in: str, check_out: str, budget_max: float = None, min_rating: float = None) -> dict:
    """
    Search for available hotels in a city.
    
    Args:
        city: City name (e.g., "Tokyo", "Hong Kong")
        check_in: Check-in date in YYYY-MM-DD format
        check_out: Check-out date in YYYY-MM-DD format
        budget_max: Maximum budget per night in USD (optional)
        min_rating: Minimum hotel rating (optional)
    
    Returns:
        dict with 'ok' status and 'data' or 'error' information
    """
    try:
        # Load hotels data
        with open('data/hotels.json', 'r') as f:
            hotels = json.load(f)
        
        # Calculate number of nights
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
        nights = (check_out_date - check_in_date).days
        
        if nights <= 0:
            return {
                "ok": False,
                "error_code": "INVALID_DATES",
                "message": "Check-out date must be after check-in date",
                "retryable": False
            }
        
        # Filter hotels
        matching_hotels = []
        for hotel in hotels:
            if hotel['city'].lower() == city.lower():
                # Check availability
                available_from = datetime.strptime(hotel['available_from'], "%Y-%m-%d")
                available_to = datetime.strptime(hotel['available_to'], "%Y-%m-%d")
                
                if check_in_date < available_from or check_out_date > available_to:
                    continue
                
                # Check rooms available
                if hotel['rooms_left'] <= 0:
                    continue
                
                # Check budget if provided
                if budget_max and hotel['price_per_night_usd'] > budget_max:
                    continue
                
                # Check rating if provided
                if min_rating and hotel['rating'] < min_rating:
                    continue
                
                matching_hotels.append(hotel)
        
        if not matching_hotels:
            return {
                "ok": False,
                "error_code": "NO_HOTEL_FOUND",
                "message": f"No available hotels found in {city} for the specified dates",
                "retryable": False
            }
        
        # Sort by rating then price
        matching_hotels.sort(key=lambda x: (-x['rating'], x['price_per_night_usd']))
        
        return {
            "ok": True,
            "data": {
                "hotels": matching_hotels[:5],
                "count": len(matching_hotels),
                "nights": nights,
                "best_value": matching_hotels[0]
            }
        }
    
    except FileNotFoundError:
        return {
            "ok": False,
            "error_code": "DATA_NOT_FOUND",
            "message": "Hotels data file not found",
            "retryable": False
        }
    except Exception as e:
        return {
            "ok": False,
            "error_code": "INTERNAL_ERROR",
            "message": f"Error searching hotels: {str(e)}",
            "retryable": True
        }

if __name__ == "__main__":
    # Test
    result = search_hotels("Tokyo", "2026-07-10", "2026-07-14")
    print(json.dumps(result, indent=2))
