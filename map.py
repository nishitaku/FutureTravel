import os
from os.path import join, dirname
from dotenv import load_dotenv

# 環境変数取得
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

# Geocoding an address
# geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# Look up an address with reverse geocoding
# reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("Sydney Town Hall",
                                     "Parramatta, NSW",
                                     mode="transit",
                                     departure_time=now)

print(directions_result)


