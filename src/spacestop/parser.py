"""
Modifed version of "apod_object_parser.py" from https://github.com/nasa/apod-api
"""

import os
from datetime import date
from typing import Any, Optional

import requests
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
API_KEY = os.getenv("NASA_APIKEY")

StartDate, EndDate = date, date
DateRange = tuple[StartDate, EndDate]


def get_data(
        date: Optional[date] = None, 
        date_range: Optional[DateRange] = None,
        count: Optional[int] = None, 
        thumbs: Optional[bool] = None,
        api_key: str = "DEMO_KEY"
        ) -> dict[str, Any]:
    params = {"api_key": api_key}
    params.update({"date": date.strftime("%Y-%m-%d")} if date else {})
    params.update({
        "start_date": date_range[0].strftime("%Y-%m-%d"),
        "end_date": date_range[1].strftime("%Y-%m-%d")
        } if date_range else {})
    params.update({"count": count} if count else {})
    params.update({"thumbs": thumbs} if thumbs else {})

    response = requests.get(f'https://api.nasa.gov/planetary/apod', params=params)
    return response.json()


def is_valid_date(in_date: date) -> bool:
    """
    Checks if the date is between today and June 16th 1995    
    """
    min_date = date(1995, 6, 16)    # first Astronomy Picture Of the Day
    max_date = date.today()
    return max_date >= in_date >= min_date


def get_specific_APOD(date: date) -> dict[str, Any]:
    return get_data(date=date, thumbs=True, api_key=API_KEY)


def get_random_APOD(count: int) -> dict[str, Any]:
    return get_data(count=count, thumbs=True, api_key=API_KEY)


def get_today_APOD() -> dict[str, Any]:
    return get_data(api_key=API_KEY)


def get_copyright(response: dict[str, Any]) -> str | None:
    copyright = response.get("copyright")
    return copyright


def get_date(response: dict[str, Any]) -> str | None:
    date = response.get("date")
    return date


def get_explaination(response: dict[str, Any]) -> str | None:
    explaination = response.get("explanation")
    return explaination


def get_hdurl(response: dict[str, Any]) -> str | None:
    hdurl = response.get("hdurl")
    return hdurl


def get_media_type(response: dict[str, Any]) -> str | None:
    media_type = response.get("media_type")
    return media_type


def get_service_version(response: dict[str, Any]) -> str | None: 
    service_version = response.get("service_version")
    return service_version


def get_thumbnail_url(response: dict[str, Any]) -> str | None:
    thumbnail_url = response.get("thumbnail_url")
    return thumbnail_url


def get_title(response: dict[str, Any]) -> str | None:
    service_version = response.get("title")
    return service_version


def get_url(response: dict[str, Any]) -> str:
    url = response.get("url")
    return url


def download_image(url: str, date: str) -> None:
    if os.path.isfile(f'{date}.png') == False:
        raw_image = requests.get(url).content
        with open(f'{date}.jpg', 'wb') as file:
            file.write(raw_image)
            
    else:
        return FileExistsError


def convert_image(image_path: str) -> None:
    path_to_image = os.path.normpath(image_path)

    basename = os.path.basename(path_to_image)

    filename_no_extension = basename.split(".")[0]

    base_directory = os.path.dirname(path_to_image)

    image = Image.open(path_to_image)
    image.save(f"{base_directory}/{filename_no_extension}.png")
