import math
import requests

#1 - address to lat and lon
def get_coordinates(address: str) -> tuple:
    response = requests.get(f"https://nominatim.openstreetmap.org/search?q={address}&format=json&limit=1")
    response.raise_for_status()
    data = response.json()[0]

    return float(data["lat"]), float(data["lon"])

#2 - lat and lon to address
def get_address(lat: float, lon: float) -> str:
    response = requests.get(f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=jsonv2")
    response.raise_for_status()
    data = response.json()
    address = data.get("display_name", "")

    return address

#3 - Haversine formula - distance in km
def haversine_distance(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = (math.sin(dlat / 2)**2) + math.cos(lat1) * math.cos(lat2) * (math.sin(dlon / 2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = 6371 * c # earth radius 6371
    
    return distance

#4 - Spherical Law of Cosines
def spherical_law_of_cosines_distance(lat1, lon1, lat2, lon2):
    R = 6371  
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_lambda = math.radians(lon2 - lon1)
    distance = math.acos(math.sin(phi1) * math.sin(phi2) + math.cos(phi1) * math.cos(phi2) * math.cos(delta_lambda)) * R
    
    return distance

#5 - Equirectangular Approximation
def equirectangular_approximation(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    x = (lon2 - lon1) * math.cos((lat1 + lat2) / 2)
    y = lat2 - lat1
    distance = math.sqrt(x**2 + y**2) * 6371

    return distance
