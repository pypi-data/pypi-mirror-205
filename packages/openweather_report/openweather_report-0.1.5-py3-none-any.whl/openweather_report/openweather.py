"""
Open Weather API Module
-----------------------

This module have classes and functions to interact with the Open Weather Map
API.
"""

import requests
from dataclasses import dataclass
from typing import Dict, Any
import json


@dataclass
class OpenWeatherMap:
    """To interface with OpenWeatherMap's API.

    This class will make API calls to get JSON data from OpenWeatherMap.
    """

    latitude: float = 0
    longitude: float = 0
    api_key: str = "NA"
    exclude: str = "NA"
    units: str = "imperial"
    language: str = "en"
    raw_data: str = "NA"

    def api_version(self, version: str) -> str:
        """API version links."""

        api_links = {
            "2.5": "http://api.openweathermap.org/data/2.5/",
            "3.0": "http://api.openweathermap.org/data/3.0/",
        }
        api_link = api_links.get(version, "Invalid")
        return api_link

    def api_call(self, api_link: str) -> None:
        """Send API request."""

        self.raw_data = json.dumps(requests.get(api_link).json())

    def by_one_call(self) -> None:
        """Pull data using the One Call API."""

        link = self.api_version("3.0")
        link += (
            f"onecall?lat={self.latitude}&lon={self.longitude}"
            + f"&units={self.units}"
            + f"&lang={self.language}"
            + f"&appid={self.api_key}"
        )
        if self.exclude != "NA":
            link += f"&exclude={self.exclude}"

        self.api_call(link)
