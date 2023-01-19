from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from services.cities import CityService
from db.base import database
from db import city


def get_city_service() -> CityService:
    return CityService(database=database, table=city)
