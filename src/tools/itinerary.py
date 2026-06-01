"""
Itinerary Builder Tool
Builds and validates travel itineraries with constraint checking.
"""

import json
from datetime import datetime

def build_itinerary(flight_ids: list, hotel_id: str, attraction_ids: list, 
                    check_in: str, check_out: str, budget_limit: float = None) -> dict:
    """
    Build a travel itinerary with constraint validation.
    
    Args:
        flight_ids: List of flight IDs (outbound and return)
        hotel_id: Hotel ID for accommodation
        attraction_ids: List of attraction IDs to visit
        check_in: Check-in date in YYYY-MM-DD format
        check_out: Check-out date in YYYY-MM-DD format
        budget_limit: Maximum total budget in USD (optional)
    
    Returns:
        dict with 'ok' status and 'data' or 'error' information
    """
    try:
        # Load data
        with open('data/flights.json', 'r') as f:
            flights = json.load(f)
        with open('data/hotels.json', 'r') as f:
            hotels = json.load(f)
        with open('data/attractions.json', 'r') as f:
            attractions = json.load(f)
        
        # Validate flights
        selected_flights = []
        for fid in flight_ids:
            flight = next((f for f in flights if f['flight_id'] == fid), None)
            if not flight:
                return {
                    "ok": False,
                    "error_code": "FLIGHT_NOT_FOUND",
                    "message": f"Flight {fid} not found",
                    "retryable": False
                }
            if flight['seats_left'] <= 0:
                return {
                    "ok": False,
                    "error_code": "NO_SEATS",
                    "message": f"Flight {fid} has no available seats",
                    "retryable": False
                }
            selected_flights.append(flight)
        
        # Validate hotel
        hotel = next((h for h in hotels if h['hotel_id'] == hotel_id), None)
        if not hotel:
            return {
                "ok": False,
                "error_code": "HOTEL_NOT_FOUND",
                "message": f"Hotel {hotel_id} not found",
                "retryable": False
            }
        if hotel['rooms_left'] <= 0:
            return {
                "ok": False,
                "error_code": "NO_ROOMS",
                "message": f"Hotel {hotel_id} has no available rooms",
                "retryable": False
            }
        
        # Calculate nights
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
        nights = (check_out_date - check_in_date).days
        
        # Validate attractions
        selected_attractions = []
        for aid in attraction_ids:
            attraction = next((a for a in attractions if a['attraction_id'] == aid), None)
            if not attraction:
                return {
                    "ok": False,
                    "error_code": "ATTRACTION_NOT_FOUND",
                    "message": f"Attraction {aid} not found",
                    "retryable": False
                }
            selected_attractions.append(attraction)
        
        # Check schedule feasibility
        total_attraction_hours = sum(a['duration_hours'] for a in selected_attractions)
        if total_attraction_hours > nights * 8:  # Max 8 hours per day
            return {
                "ok": False,
                "error_code": "SCHEDULE_CONFLICT",
                "message": f"Too many attractions: {total_attraction_hours} hours for {nights} days",
                "retryable": False
            }
        
        # Calculate total cost
        flight_cost = sum(f['price_usd'] for f in selected_flights)
        hotel_cost = hotel['price_per_night_usd'] * nights
        attraction_cost = sum(a['ticket_price_usd'] for a in selected_attractions)
        total_cost = flight_cost + hotel_cost + attraction_cost
        
        # Check budget
        if budget_limit and total_cost > budget_limit:
            return {
                "ok": False,
                "error_code": "BUDGET_EXCEEDED",
                "message": f"Total cost ${total_cost:.2f} exceeds budget ${budget_limit:.2f}",
                "retryable": False,
                "data": {
                    "total_cost_usd": total_cost,
                    "budget_limit": budget_limit,
                    "over_budget_by": total_cost - budget_limit
                }
            }
        
        # Build itinerary
        itinerary = {
            "flights": selected_flights,
            "hotel": hotel,
            "attractions": selected_attractions,
            "dates": {
                "check_in": check_in,
                "check_out": check_out,
                "nights": nights
            },
            "cost_breakdown": {
                "flights": flight_cost,
                "hotel": hotel_cost,
                "attractions": attraction_cost,
                "total": total_cost
            },
            "status": "valid" if total_cost <= (budget_limit or float('inf')) else "over_budget"
        }
        
        return {
            "ok": True,
            "data": itinerary
        }
    
    except FileNotFoundError as e:
        return {
            "ok": False,
            "error_code": "DATA_NOT_FOUND",
            "message": f"Data file not found: {str(e)}",
            "retryable": False
        }
    except Exception as e:
        return {
            "ok": False,
            "error_code": "INTERNAL_ERROR",
            "message": f"Error building itinerary: {str(e)}",
            "retryable": True
        }

def estimate_trip_total(flight_ids: list, hotel_id: str, attraction_ids: list, 
                       check_in: str, check_out: str, transport_style: str = "normal") -> dict:
    """
    Estimate total trip cost including transportation.
    
    Args:
        flight_ids: List of flight IDs
        hotel_id: Hotel ID
        attraction_ids: List of attraction IDs
        check_in: Check-in date
        check_out: Check-out date
        transport_style: Transport style (budget/normal/comfort)
    
    Returns:
        dict with cost breakdown
    """
    try:
        # Build base itinerary
        result = build_itinerary(flight_ids, hotel_id, attraction_ids, check_in, check_out)
        
        if not result['ok']:
            return result
        
        itinerary = result['data']
        nights = itinerary['dates']['nights']
        city = itinerary['hotel']['city']
        
        # Add transport cost
        from .transport import estimate_local_transport
        transport_result = estimate_local_transport(city, nights, transport_style)
        
        if transport_result['ok']:
            transport_cost = transport_result['data']['total_cost_usd']
            itinerary['cost_breakdown']['transport'] = transport_cost
            itinerary['cost_breakdown']['total'] += transport_cost
            itinerary['transport'] = transport_result['data']
        
        return {
            "ok": True,
            "data": itinerary
        }
    
    except Exception as e:
        return {
            "ok": False,
            "error_code": "INTERNAL_ERROR",
            "message": f"Error estimating trip total: {str(e)}",
            "retryable": True
        }

if __name__ == "__main__":
    # Test
    result = build_itinerary(
        flight_ids=["FL-001", "FL-001"],
        hotel_id="HT-101",
        attraction_ids=["AT-501", "AT-502"],
        check_in="2026-07-10",
        check_out="2026-07-14",
        budget_limit=2000
    )
    print(json.dumps(result, indent=2))
