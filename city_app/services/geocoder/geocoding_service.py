from geopy.geocoders import Nominatim
from django.contrib.gis.geos import Point


class GeocodingService:
    """
    A service class for geocoding city names into geographic coordinates using the Nominatim API.
    """

    def __init__(self, user_agent="city_api"):
        """
        Initializes the GeocodingService with a specified user agent for Nominatim API requests.

        Args:
            user_agent (str): The user agent string to be used for requests. Default is "city_api".
        """
        self.geolocator = Nominatim(user_agent=user_agent)

    def get_location(self, city_name: str) -> Point:
        """
        Converts a city name into geographic coordinates (latitude and longitude).

        Args:
            city_name (str): The name of the city to geocode.

        Returns:
            Point: A Point object containing the longitude and latitude of the city.

        Raises:
            ValueError: If the location cannot be found for the given city name.
        """
        location = self.geolocator.geocode(city_name)
        if location is None:
            raise ValueError(f"Could not find location for the city: {city_name}")
        return Point(location.longitude, location.latitude)
