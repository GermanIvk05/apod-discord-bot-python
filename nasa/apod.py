from datetime import date
from typing import Optional, Dict, Any, List

import requests


class APODError(Exception):
    """Base exception class for APOD-related errors."""
    pass


class DateOutOfRangeError(APODError):
    """Exception raised when the specified date is out of the allowed range."""
    pass


class StartDateAfterEndDateError(APODError):
    """Exception raised when the start date is after the end date."""
    pass


class APIDataFetchError(APODError):
    """Exception raised when there is an error fetching data from the APOD API."""
    pass


def validate_date(date_to_validate: date, start: date = date(1995, 6, 16), end: date = date.today()) -> date:
    """Validate if the date is within the specified range."""
    if not start <= date_to_validate <= end:
        raise DateOutOfRangeError("The date must be between June 16th, 1995, and today.")
    return date_to_validate


class APODClient:
    BASE_URL = 'https://api.nasa.gov/planetary/apod'

    def __init__(self, key: str) -> None:
        self.session = requests.Session()
        self.key = key

    def _fetch(self, params: Dict[str, Any]) -> Any:
        try:
            response = self.session.get(self.BASE_URL, params=params)
            response.raise_for_status()
        except requests.RequestException as e:
            raise APIDataFetchError(f"Failed to fetch data: {e}") from e
        return response.json()

    def _build_params(self, **kwargs) -> Dict[str, Any]:
        params = {'api_key': self.key}
        params.update({
            k: validate_date(v).isoformat() if isinstance(v, date) else v
            for k, v in kwargs.items() if v is not None
        })
        return params

    def get(self, when: Optional[date] = None, thumbs: bool = False) -> Dict[str, Any]:
        params = self._build_params(date=when, thumbs=thumbs)
        return self._fetch(params)

    def get_list(self, start: date, end: Optional[date] = None, thumbs: bool = False) -> List[Dict[str, Any]]:
        if start > (end or date.today()):
            raise StartDateAfterEndDateError("The start date cannot be after the end date.")
        params = self._build_params(start_date=start, end_date=end, thumbs=thumbs)
        return self._fetch(params)

    def get_random(self, count: int, thumbs: bool = False) -> List[Dict[str, Any]]:
        params = self._build_params(count=count, thumbs=thumbs)
        return self._fetch(params)

    def __del__(self):
        self.session.close()
