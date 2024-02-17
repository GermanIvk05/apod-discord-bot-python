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


class APODClient:
    BASE_URL = 'https://api.nasa.gov/planetary/apod'

    def __init__(self, key: str):
        self.session = requests.Session()
        self.key = key

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def _fetch(self, params: Dict[str, Any]) -> Any:
        try:
            response = self.session.get(self.BASE_URL, params=params)
            response.raise_for_status()
        except requests.RequestException as e:
            raise APIDataFetchError(f"Failed to fetch data: {e}") from e
        return response.json()

    def _build_params(self, **kwargs) -> Dict[str, Any]:
        upper_bound = date.today()
        lower_bound = date(1995, 6, 16)

        params = {'api_key': self.key}
        params.update({
            k: v.isoformat() if isinstance(v, date) and upper_bound >= v >= lower_bound else v
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
        if count < 1:
            raise ValueError('Counter must be a positive integer.')
        params = self._build_params(count=count, thumbs=thumbs)
        return self._fetch(params)
