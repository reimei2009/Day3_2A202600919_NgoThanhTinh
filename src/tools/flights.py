"""
Flight Search Tool
Searches for available flights based on origin, destination, and dates.
"""

import json
from datetime import datetime

def search_flights(origin: str, destination: str, depart_date: str, budget_max: float = None) -> dict:
    """
    Search for available flights matching the criteria.
    
    Args:
        origin: Origin airport code (e.g., "SGN", "HAN")
        destination: Destination airport code (e.g., "NRT", "HKG")
        depart_date: Departure date in YYYY-MM-DD format
        budget_max: Maximum budget in USD (optional)
    
    Returns:
        dict with 'ok' status and 'data' or 'error' information
    """
    try:
        # Load flights data
        with open('data/flights.json', 'r') as f:
            flights = json.load(f)
        
        # Filter flights
        matching_flights = []
        for flight in flights:
            if (flight['origin'].upper() == origin.upper() and 
                flight['destination'].upper() == destination.upper() and
                flight['depart_date'] == depart_date):
                
                # Check budget if provided
                if budget_max and flight['price_usd'] > budget_max:
                    continue
                
                # Check availability
                if flight['seats_left'] > 0:
                    matching_flights.append(flight)
        
        if not matching_flights:
            return {
                "ok": False,
                "error_code": "NO_FLIGHT_FOUND",
                "message": f"No available flights found from {origin} to {destination} on {depart_date}",
                "retryable": False
            }
        
        # Sort by price
        matching_flights.sort(key=lambda x: x['price_usd'])
        
        return {
            "ok": True,
            "data": {
                "flights": matching_flights[:5],  # Return top 5 options
                "count": len(matching_flights),
                "cheapest": matching_flights[0]['price_usd']
            }
        }
    
    except FileNotFoundError:
        return {
            "ok": False,
            "error_code": "DATA_NOT_FOUND",
            "message": "Flights data file not found",
            "retryable": False
        }
    except Exception as e:
        return {
            "ok": False,
            "error_code": "INTERNAL_ERROR",
            "message": f"Error searching flights: {str(e)}",
            "retryable": True
        }

if __name__ == "__main__":
    # Test
    result = search_flights("SGN", "NRT", "2026-07-10")
    print(json.dumps(result, indent=2))
