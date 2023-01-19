import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends

from models.cities import CityModel
from models.city_weathers import CityWeather, WeatherStatistic
from services.cities import CityService
from .depends import get_city_service

router = APIRouter()


@router.post("/weather/{city}", response_model=CityModel)
async def create_city(
        city: str,
        cities: CityService = Depends(get_city_service)
):
    return await cities.create(name=city)


@router.get("/last_weather", response_model=List[CityWeather])
async def last_weather(
        search: Optional[str] = None,
        cities: CityService = Depends(get_city_service)
):
    return await cities.get_last_weather(search=search)


@router.get("/city_stats", response_model=WeatherStatistic)
async def statistics(
        city: str,
        date_start: datetime.date,
        date_end: datetime.date,
        cities: CityService = Depends(get_city_service)
):
    return await cities.get_statistics(city_name=city, date_start=date_start, date_end=date_end)
