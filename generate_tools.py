import os

# Create flights tool
flights_tool = '''"""
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
'''

# Create hotels tool
hotels_tool = '''"""
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
'''

# Create attractions tool
attractions_tool = '''"""
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
'''

# Create weather tool
weather_tool = '''"""
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
'''

# Create transport tool
transport_tool = '''"""
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
'''

# Create itinerary tool
itinerary_tool = '''"""
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
'''

# Write all tool files
tools = {
    'src/tools/flights.py': flights_tool,
    'src/tools/hotels.py': hotels_tool,
    'src/tools/attractions.py': attractions_tool,
    'src/tools/weather.py': weather_tool,
    'src/tools/transport.py': transport_tool,
    'src/tools/itinerary.py': itinerary_tool
}

for filepath, content in tools.items():
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"✅ Created {filepath}")

print("\n🎉 All tools created successfully!")