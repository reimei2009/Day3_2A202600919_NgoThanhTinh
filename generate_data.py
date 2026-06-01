import json
import os

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Generate flights.json
flights = [
    {"flight_id": "FL-001", "origin": "SGN", "destination": "NRT", "depart_date": "2026-07-10", "return_date": "2026-07-14", "airline": "VN Air", "stops": 1, "duration_hours": 8.5, "price_usd": 420, "seats_left": 5},
    {"flight_id": "FL-002", "origin": "SGN", "destination": "NRT", "depart_date": "2026-07-10", "return_date": "2026-07-14", "airline": "JAL", "stops": 0, "duration_hours": 6.0, "price_usd": 680, "seats_left": 3},
    {"flight_id": "FL-003", "origin": "SGN", "destination": "NRT", "depart_date": "2026-07-10", "return_date": "2026-07-14", "airline": "ANA", "stops": 0, "duration_hours": 5.8, "price_usd": 720, "seats_left": 2},
    {"flight_id": "FL-004", "origin": "SGN", "destination": "HKG", "depart_date": "2026-07-10", "return_date": "2026-07-14", "airline": "VietJet", "stops": 0, "duration_hours": 2.5, "price_usd": 180, "seats_left": 0},
    {"flight_id": "FL-005", "origin": "SGN", "destination": "HKG", "depart_date": "2026-07-10", "return_date": "2026-07-14", "airline": "Cathay", "stops": 0, "duration_hours": 2.3, "price_usd": 320, "seats_left": 8},
    {"flight_id": "FL-006", "origin": "SGN", "destination": "BKK", "depart_date": "2026-07-10", "return_date": "2026-07-14", "airline": "Thai Air", "stops": 0, "duration_hours": 1.8, "price_usd": 150, "seats_left": 12},
    {"flight_id": "FL-007", "origin": "SGN", "destination": "BKK", "depart_date": "2026-07-10", "return_date": "2026-07-14", "airline": "VietJet", "stops": 0, "duration_hours": 1.9, "price_usd": 120, "seats_left": 20},
    {"flight_id": "FL-008", "origin": "SGN", "destination": "SIN", "depart_date": "2026-07-10", "return_date": "2026-07-14", "airline": "Singapore Air", "stops": 0, "duration_hours": 2.2, "price_usd": 380, "seats_left": 6},
    {"flight_id": "FL-009", "origin": "SGN", "destination": "SIN", "depart_date": "2026-07-10", "return_date": "2026-07-14", "airline": "VietJet", "stops": 0, "duration_hours": 2.3, "price_usd": 200, "seats_left": 15},
    {"flight_id": "FL-010", "origin": "SGN", "destination": "NRT", "depart_date": "2026-07-15", "return_date": "2026-07-19", "airline": "VN Air", "stops": 1, "duration_hours": 8.5, "price_usd": 450, "seats_left": 4},
    {"flight_id": "FL-011", "origin": "SGN", "destination": "NRT", "depart_date": "2026-07-15", "return_date": "2026-07-19", "airline": "JAL", "stops": 0, "duration_hours": 6.0, "price_usd": 700, "seats_left": 2},
    {"flight_id": "FL-012", "origin": "SGN", "destination": "HKG", "depart_date": "2026-07-15", "return_date": "2026-07-19", "airline": "Cathay", "stops": 0, "duration_hours": 2.3, "price_usd": 340, "seats_left": 7},
    {"flight_id": "FL-013", "origin": "SGN", "destination": "BKK", "depart_date": "2026-07-15", "return_date": "2026-07-19", "airline": "Thai Air", "stops": 0, "duration_hours": 1.8, "price_usd": 160, "seats_left": 10},
    {"flight_id": "FL-014", "origin": "SGN", "destination": "SIN", "depart_date": "2026-07-15", "return_date": "2026-07-19", "airline": "Singapore Air", "stops": 0, "duration_hours": 2.2, "price_usd": 400, "seats_left": 5},
    {"flight_id": "FL-015", "origin": "SGN", "destination": "NRT", "depart_date": "2026-08-01", "return_date": "2026-08-07", "airline": "VN Air", "stops": 1, "duration_hours": 8.5, "price_usd": 480, "seats_left": 6},
    {"flight_id": "FL-016", "origin": "SGN", "destination": "NRT", "depart_date": "2026-08-01", "return_date": "2026-08-07", "airline": "ANA", "stops": 0, "duration_hours": 5.8, "price_usd": 780, "seats_left": 1},
    {"flight_id": "FL-017", "origin": "SGN", "destination": "HKG", "depart_date": "2026-08-01", "return_date": "2026-08-07", "airline": "Cathay", "stops": 0, "duration_hours": 2.3, "price_usd": 350, "seats_left": 9},
    {"flight_id": "FL-018", "origin": "SGN", "destination": "BKK", "depart_date": "2026-08-01", "return_date": "2026-08-07", "airline": "VietJet", "stops": 0, "duration_hours": 1.9, "price_usd": 130, "seats_left": 25},
    {"flight_id": "FL-019", "origin": "SGN", "destination": "SIN", "depart_date": "2026-08-01", "return_date": "2026-08-07", "airline": "Singapore Air", "stops": 0, "duration_hours": 2.2, "price_usd": 420, "seats_left": 8},
    {"flight_id": "FL-020", "origin": "HAN", "destination": "NRT", "depart_date": "2026-07-10", "return_date": "2026-07-14", "airline": "VN Air", "stops": 1, "duration_hours": 7.5, "price_usd": 400, "seats_left": 3},
    {"flight_id": "FL-021", "origin": "HAN", "destination": "HKG", "depart_date": "2026-07-10", "return_date": "2026-07-14", "airline": "VietJet", "stops": 0, "duration_hours": 2.0, "price_usd": 170, "seats_left": 10},
    {"flight_id": "FL-022", "origin": "HAN", "destination": "BKK", "depart_date": "2026-07-10", "return_date": "2026-07-14", "airline": "Thai Air", "stops": 0, "duration_hours": 1.5, "price_usd": 140, "seats_left": 14},
    {"flight_id": "FL-023", "origin": "HAN", "destination": "SIN", "depart_date": "2026-07-10", "return_date": "2026-07-14", "airline": "Singapore Air", "stops": 1, "duration_hours": 3.5, "price_usd": 360, "seats_left": 7},
    {"flight_id": "FL-024", "origin": "HAN", "destination": "NRT", "depart_date": "2026-07-15", "return_date": "2026-07-19", "airline": "VN Air", "stops": 1, "duration_hours": 7.5, "price_usd": 430, "seats_left": 2},
    {"flight_id": "FL-025", "origin": "HAN", "destination": "HKG", "depart_date": "2026-07-15", "return_date": "2026-07-19", "airline": "Cathay", "stops": 0, "duration_hours": 1.9, "price_usd": 310, "seats_left": 6},
    {"flight_id": "FL-026", "origin": "HAN", "destination": "BKK", "depart_date": "2026-07-15", "return_date": "2026-07-19", "airline": "Thai Air", "stops": 0, "duration_hours": 1.5, "price_usd": 150, "seats_left": 11},
    {"flight_id": "FL-027", "origin": "HAN", "destination": "SIN", "depart_date": "2026-07-15", "return_date": "2026-07-19", "airline": "Singapore Air", "stops": 1, "duration_hours": 3.5, "price_usd": 380, "seats_left": 4},
    {"flight_id": "FL-028", "origin": "HAN", "destination": "NRT", "depart_date": "2026-08-01", "return_date": "2026-08-07", "airline": "VN Air", "stops": 1, "duration_hours": 7.5, "price_usd": 460, "seats_left": 5},
    {"flight_id": "FL-029", "origin": "HAN", "destination": "HKG", "depart_date": "2026-08-01", "return_date": "2026-08-07", "airline": "Cathay", "stops": 0, "duration_hours": 1.9, "price_usd": 330, "seats_left": 8},
    {"flight_id": "FL-030", "origin": "HAN", "destination": "BKK", "depart_date": "2026-08-01", "return_date": "2026-08-07", "airline": "VietJet", "stops": 0, "duration_hours": 1.6, "price_usd": 125, "seats_left": 18}
]

with open('data/flights.json', 'w') as f:
    json.dump(flights, f, indent=2)
print("✅ Created data/flights.json with 30 flights")

# Generate hotels.json
hotels = [
    {"hotel_id": "HT-101", "city": "Tokyo", "name": "Ueno Stay", "price_per_night_usd": 68, "rating": 4.2, "area": "Ueno", "distance_to_center_km": 3.1, "available_from": "2026-07-01", "available_to": "2026-08-31", "rooms_left": 7},
    {"hotel_id": "HT-102", "city": "Tokyo", "name": "Shinjuku Grand", "price_per_night_usd": 180, "rating": 4.8, "area": "Shinjuku", "distance_to_center_km": 0.5, "available_from": "2026-07-01", "available_to": "2026-08-31", "rooms_left": 0},
    {"hotel_id": "HT-103", "city": "Tokyo", "name": "Asakusa Ryokan", "price_per_night_usd": 95, "rating": 4.5, "area": "Asakusa", "distance_to_center_km": 4.2, "available_from": "2026-07-01", "available_to": "2026-08-31", "rooms_left": 5},
    {"hotel_id": "HT-104", "city": "Tokyo", "name": "Ginza Luxury", "price_per_night_usd": 320, "rating": 4.9, "area": "Ginza", "distance_to_center_km": 0.8, "available_from": "2026-07-01", "available_to": "2026-08-31", "rooms_left": 3},
    {"hotel_id": "HT-105", "city": "Tokyo", "name": "Ikebukuro Inn", "price_per_night_usd": 75, "rating": 4.1, "area": "Ikebukuro", "distance_to_center_km": 3.5, "available_from": "2026-07-01", "available_to": "2026-08-31", "rooms_left": 12},
    {"hotel_id": "HT-106", "city": "Hong Kong", "name": "Tsim Sha Tsui View", "price_per_night_usd": 150, "rating": 4.6, "area": "TST", "distance_to_center_km": 1.2, "available_from": "2026-07-01", "available_to": "2026-08-31", "rooms_left": 8},
    {"hotel_id": "HT-107", "city": "Hong Kong", "name": "Central Business", "price_per_night_usd": 280, "rating": 4.7, "area": "Central", "distance_to_center_km": 0.3, "available_from": "2026-07-01", "available_to": "2026-08-31", "rooms_left": 4},
    {"hotel_id": "HT-108", "city": "Hong Kong", "name": "Mong Kok Budget", "price_per_night_usd": 85, "rating": 3.9, "area": "Mong Kok", "distance_to_center_km": 2.5, "available_from": "2026-07-01", "available_to": "2026-08-31", "rooms_left": 15},
    {"hotel_id": "HT-109", "city": "Hong Kong", "name": "Causeway Bay Suite", "price_per_night_usd": 220, "rating": 4.5, "area": "Causeway Bay", "distance_to_center_km": 2.0, "available_from": "2026-07-01", "available_to": "2026-08-31", "rooms_left": 6},
    {"hotel_id": "HT-110", "city": "Bangkok", "name": "Sukhumvit Stay", "price_per_night_usd": 65, "rating": 4.3, "area": "Sukhumvit", "distance_to_center_km": 3.8, "available_from": "2026-07-01", "available_to": "2026-08-31", "rooms_left": 20},
    {"hotel_id": "HT-111", "city": "Bangkok", "name": "Silom Business", "price_per_night_usd": 110, "rating": 4.4, "area": "Silom", "distance_to_center_km": 2.5, "available_from": "2026-07-01", "available_to": "2026-08-31", "rooms_left": 10},
    {"hotel_id": "HT-112", "city": "Bangkok", "name": "Khao San Backpacker", "price_per_night_usd": 35, "rating": 3.8, "area": "Khao San", "distance_to_center_km": 1.5, "available_from": "2026-07-01", "available_to": "2026-08-31", "rooms_left": 30},
    {"hotel_id": "HT-113", "city": "Bangkok", "name": "Siam Luxury", "price_per_night_usd": 180, "rating": 4.7, "area": "Siam", "distance_to_center_km": 1.8, "available_from": "2026-07-01", "available_to": "2026-08-31", "rooms_left": 5},
    {"hotel_id": "HT-114", "city": "Bangkok", "name": "Riverside Resort", "price_per_night_usd": 145, "rating": 4.5, "area": "Riverside", "distance_to_center_km": 4.0, "available_from": "2026-07-01", "available_to": "2026-08-31", "rooms_left": 8},
    {"hotel_id": "HT-115", "city": "Singapore", "name": "Marina Bay View", "price_per_night_usd": 350, "rating": 4.9, "area": "Marina Bay", "distance_to_center_km": 0.5, "available_from": "2026-07-01", "available_to": "2026-08-31", "rooms_left": 3},
    {"hotel_id": "HT-116", "city": "Singapore", "name": "Orchard Road Stay", "price_per_night_usd": 220, "rating": 4.6, "area": "Orchard", "distance_to_center_km": 1.2, "available_from": "2026-07-01", "available_to": "2026-08-31", "rooms_left": 7},
    {"hotel_id": "HT-117", "city": "Singapore", "name": "Chinatown Heritage", "price_per_night_usd": 120, "rating": 4.4, "area": "Chinatown", "distance_to_center_km": 2.0, "available_from": "2026-07-01", "available_to": "2026-08-31", "rooms_left": 12},
    {"hotel_id": "HT-118", "city": "Singapore", "name": "Little India Inn", "price_per_night_usd": 95, "rating": 4.2, "area": "Little India", "distance_to_center_km": 3.5, "available_from": "2026-07-01", "available_to": "2026-08-31", "rooms_left": 15},
    {"hotel_id": "HT-119", "city": "Singapore", "name": "Sentosa Resort", "price_per_night_usd": 280, "rating": 4.7, "area": "Sentosa", "distance_to_center_km": 6.0, "available_from": "2026-07-01", "available_to": "2026-08-31", "rooms_left": 6},
    {"hotel_id": "HT-120", "city": "Singapore", "name": "Clarke Quay Budget", "price_per_night_usd": 85, "rating": 4.0, "area": "Clarke Quay", "distance_to_center_km": 1.8, "available_from": "2026-07-01", "available_to": "2026-08-31", "rooms_left": 18}
]

with open('data/hotels.json', 'w') as f:
    json.dump(hotels, f, indent=2)
print("✅ Created data/hotels.json with 20 hotels")

# Generate attractions.json
attractions = [
    {"attraction_id": "AT-501", "city": "Tokyo", "name": "Tokyo National Museum", "tags": ["museum", "history", "indoor"], "ticket_price_usd": 8, "duration_hours": 2.0, "open_hours": {"open": "09:30", "close": "17:00"}, "closed_weekdays": ["MON"], "area": "Ueno"},
    {"attraction_id": "AT-502", "city": "Tokyo", "name": "Senso-ji Temple", "tags": ["temple", "culture", "outdoor"], "ticket_price_usd": 0, "duration_hours": 1.5, "open_hours": {"open": "06:00", "close": "17:00"}, "closed_weekdays": [], "area": "Asakusa"},
    {"attraction_id": "AT-503", "city": "Tokyo", "name": "Tokyo Skytree", "tags": ["landmark", "view", "outdoor"], "ticket_price_usd": 25, "duration_hours": 2.5, "open_hours": {"open": "08:00", "close": "22:00"}, "closed_weekdays": [], "area": "Sumida"},
    {"attraction_id": "AT-504", "city": "Tokyo", "name": "Shinjuku Gyoen", "tags": ["park", "nature", "outdoor"], "ticket_price_usd": 3, "duration_hours": 2.0, "open_hours": {"open": "09:00", "close": "16:30"}, "closed_weekdays": ["MON"], "area": "Shinjuku"},
    {"attraction_id": "AT-505", "city": "Tokyo", "name": "Meiji Shrine", "tags": ["shrine", "culture", "outdoor"], "ticket_price_usd": 0, "duration_hours": 1.0, "open_hours": {"open": "05:00", "close": "18:00"}, "closed_weekdays": [], "area": "Shibuya"},
    {"attraction_id": "AT-506", "city": "Hong Kong", "name": "Victoria Peak", "tags": ["landmark", "view", "outdoor"], "ticket_price_usd": 12, "duration_hours": 2.0, "open_hours": {"open": "07:00", "close": "23:00"}, "closed_weekdays": [], "area": "Mid-Levels"},
    {"attraction_id": "AT-507", "city": "Hong Kong", "name": "Disneyland", "tags": ["theme park", "family", "outdoor"], "ticket_price_usd": 85, "duration_hours": 8.0, "open_hours": {"open": "10:00", "close": "21:00"}, "closed_weekdays": [], "area": "Lantau"},
    {"attraction_id": "AT-508", "city": "Hong Kong", "name": "Tian Tan Buddha", "tags": ["statue", "culture", "outdoor"], "ticket_price_usd": 15, "duration_hours": 3.0, "open_hours": {"open": "10:00", "close": "18:00"}, "closed_weekdays": [], "area": "Lantau"},
    {"attraction_id": "AT-509", "city": "Hong Kong", "name": "Ocean Park", "tags": ["theme park", "aquarium", "outdoor"], "ticket_price_usd": 60, "duration_hours": 6.0, "open_hours": {"open": "10:00", "close": "18:00"}, "closed_weekdays": [], "area": "Southern"},
    {"attraction_id": "AT-510", "city": "Hong Kong", "name": "Museum of History", "tags": ["museum", "history", "indoor"], "ticket_price_usd": 8, "duration_hours": 2.0, "open_hours": {"open": "10:00", "close": "18:00"}, "closed_weekdays": ["TUE"], "area": "TST"},
    {"attraction_id": "AT-511", "city": "Bangkok", "name": "Grand Palace", "tags": ["palace", "culture", "outdoor"], "ticket_price_usd": 15, "duration_hours": 2.5, "open_hours": {"open": "08:30", "close": "15:30"}, "closed_weekdays": [], "area": "Old City"},
    {"attraction_id": "AT-512", "city": "Bangkok", "name": "Wat Pho", "tags": ["temple", "culture", "outdoor"], "ticket_price_usd": 5, "duration_hours": 1.5, "open_hours": {"open": "08:00", "close": "18:00"}, "closed_weekdays": [], "area": "Old City"},
    {"attraction_id": "AT-513", "city": "Bangkok", "name": "Chatuchak Market", "tags": ["market", "shopping", "outdoor"], "ticket_price_usd": 0, "duration_hours": 3.0, "open_hours": {"open": "09:00", "close": "18:00"}, "closed_weekdays": ["MON", "TUE"], "area": "Chatuchak"},
    {"attraction_id": "AT-514", "city": "Bangkok", "name": "Siam Paragon", "tags": ["mall", "shopping", "indoor"], "ticket_price_usd": 0, "duration_hours": 3.0, "open_hours": {"open": "10:00", "close": "22:00"}, "closed_weekdays": [], "area": "Siam"},
    {"attraction_id": "AT-515", "city": "Bangkok", "name": "Jim Thompson House", "tags": ["museum", "history", "indoor"], "ticket_price_usd": 10, "duration_hours": 1.5, "open_hours": {"open": "09:00", "close": "17:00"}, "closed_weekdays": [], "area": "Silom"},
    {"attraction_id": "AT-516", "city": "Singapore", "name": "Gardens by the Bay", "tags": ["garden", "nature", "outdoor"], "ticket_price_usd": 28, "duration_hours": 3.0, "open_hours": {"open": "05:00", "close": "02:00"}, "closed_weekdays": [], "area": "Marina Bay"},
    {"attraction_id": "AT-517", "city": "Singapore", "name": "Marina Bay Sands", "tags": ["landmark", "view", "outdoor"], "ticket_price_usd": 23, "duration_hours": 2.0, "open_hours": {"open": "09:30", "close": "22:00"}, "closed_weekdays": [], "area": "Marina Bay"},
    {"attraction_id": "AT-518", "city": "Singapore", "name": "Universal Studios", "tags": ["theme park", "family", "outdoor"], "ticket_price_usd": 81, "duration_hours": 8.0, "open_hours": {"open": "10:00", "close": "19:00"}, "closed_weekdays": [], "area": "Sentosa"},
    {"attraction_id": "AT-519", "city": "Singapore", "name": "Botanic Gardens", "tags": ["garden", "nature", "outdoor"], "ticket_price_usd": 0, "duration_hours": 2.5, "open_hours": {"open": "05:00", "close": "24:00"}, "closed_weekdays": [], "area": "Central"},
    {"attraction_id": "AT-520", "city": "Singapore", "name": "Asian Civilisations Museum", "tags": ["museum", "history", "indoor"], "ticket_price_usd": 10, "duration_hours": 2.0, "open_hours": {"open": "10:00", "close": "19:00"}, "closed_weekdays": ["MON"], "area": "Civic District"}
]

with open('data/attractions.json', 'w') as f:
    json.dump(attractions, f, indent=2)
print("✅ Created data/attractions.json with 20 attractions")

# Generate transport_rules.json
transport_rules = {
    "Tokyo": {"budget": {"daily_usd": 10}, "normal": {"daily_usd": 18}, "comfort": {"daily_usd": 35}},
    "Hong Kong": {"budget": {"daily_usd": 8}, "normal": {"daily_usd": 15}, "comfort": {"daily_usd": 30}},
    "Bangkok": {"budget": {"daily_usd": 6}, "normal": {"daily_usd": 12}, "comfort": {"daily_usd": 25}},
    "Singapore": {"budget": {"daily_usd": 12}, "normal": {"daily_usd": 20}, "comfort": {"daily_usd": 40}}
}

with open('data/transport_rules.json', 'w') as f:
    json.dump(transport_rules, f, indent=2)
print("✅ Created data/transport_rules.json")

# Generate weather.json
import datetime

weather_data = []
cities = ["Tokyo", "Hong Kong", "Bangkok", "Singapore"]
base_date = datetime.date(2026, 7, 10)

conditions = ["sunny", "cloudy", "rain", "partly_cloudy"]

for city in cities:
    for i in range(30):
        date = base_date + datetime.timedelta(days=i)
        # Add some rainy days for edge cases
        if city == "Tokyo" and i in [5, 6, 18, 19]:
            condition = "rain"
        elif city == "Hong Kong" and i in [7, 8, 20, 21]:
            condition = "rain"
        else:
            condition = conditions[i % len(conditions)]
        
        weather_data.append({
            "city": city,
            "date": date.strftime("%Y-%m-%d"),
            "condition": condition,
            "temp_c_min": 24 + (i % 8),
            "temp_c_max": 30 + (i % 6)
        })

with open('data/weather.json', 'w') as f:
    json.dump(weather_data, f, indent=2)
print("✅ Created data/weather.json with 120 weather records")

# Generate scenarios.json for edge cases
scenarios = [
    {"scenario_id": "SC-001", "name": "No Available Flights", "description": "Flight exists but seats_left = 0"},
    {"scenario_id": "SC-002", "name": "No Available Hotels", "description": "Hotel in budget but rooms_left = 0"},
    {"scenario_id": "SC-003", "name": "Attraction Closed", "description": "Attraction closed on requested day"},
    {"scenario_id": "SC-004", "name": "Rainy Day Plan", "description": "Rainy day with mostly outdoor plan"},
    {"scenario_id": "SC-005", "name": "Budget Exceeded", "description": "Total trip cost exceeds budget"}
]

with open('data/scenarios.json', 'w') as f:
    json.dump(scenarios, f, indent=2)
print("✅ Created data/scenarios.json with edge case scenarios")

print("\n🎉 All synthetic datasets generated successfully!")