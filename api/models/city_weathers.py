import datetime
from typing import List

from pydantic import BaseModel


class CityWeather(BaseModel):
    id: int
    name: str
    temperature: int
    pressure: int
    wind_speed: float
    datetime: datetime.datetime


class AvgStat(BaseModel):
    avg_temperature: float
    avg_pressure: float
    avg_wind_speed: float


class CityStatistics(BaseModel):
    temperature: int
    pressure: int
    wind_speed: float
    datetime: datetime.datetime


class WeatherStatistics(AvgStat):
    id: int
    name: str
    statistics: List[CityStatistics]

