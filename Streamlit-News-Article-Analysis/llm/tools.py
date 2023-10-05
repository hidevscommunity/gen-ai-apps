import numpy as np
import os
from dotenv import load_dotenv
import os
from collections import deque
from typing import Dict, List, Optional, Any
from geopy.geocoders import Nominatim
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

def get_coordinates(location:str) -> tuple[float, float]:
    """Returns the latitude and longitude of a location.Location should include any landmarks,cities, countries and addresses, output an address searchable in googleMaps be as specific as possible."""
    geolocator = Nominatim(user_agent="geoapi_explorer")
    try:
        location_info = geolocator.geocode(location)
    except:
        return "Location Output must be more general, Must Only return Country/City of disruption event as location"
    
    if location_info:
        latitude = location_info.latitude
        longitude = location_info.longitude
        return (latitude, longitude)
    else:
        return "Location Output must be more general, Must Only return Country/City of disruption event as location"