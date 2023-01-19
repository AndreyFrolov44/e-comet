import datetime

from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func

from .base import metadata


city = Table(
    'cities',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, unique=True, nullable=False, index=True),
    Column('lat', Float, unique=True, nullable=False, index=True),
    Column('lon', Float, unique=True, nullable=False, index=True),
)

city_weather = Table(
    'city_weathers',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('city_id', Integer, ForeignKey('cities.id', ondelete='CASCADE'), index=True, nullable=False),
    Column('temperature', Integer, nullable=False),
    Column('pressure', Integer, nullable=False),
    Column('wind_speed', Float, nullable=False),
    Column('datetime', DateTime, nullable=False, default=func.now(), server_default=func.now())
)


