from pydantic import BaseModel
from typing import Optional


class CityModel(BaseModel):
    id: Optional[int]
    name: str
    lat: float
    lon: float
