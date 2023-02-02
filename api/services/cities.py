import datetime
import json
from typing import Optional, List

from fastapi import HTTPException, status

from models.city_weathers import CityWeather, AvgStat, WeatherStatistics, CityStatistics
from services.base import BaseService
from models.cities import CityModel
from db import city
from uttils import run_city


class CityService(BaseService):
    async def create(self, name: str) -> CityModel:
        if await self.get(city.c.name == name):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Данный город уже добавлен')

        run_city(city=name)

        with open('city.json', 'r+') as f:
            data = json.loads(f.read())
            f.truncate(0)

        city_data = data[0]
        if city_data['id'] is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Город не найден')

        new = CityModel(name=name, id=city_data['id'], lat=city_data['lat'], lon=city_data['lon'])
        await super().create(name=name, id=city_data['id'], lat=city_data['lat'], lon=city_data['lon'])
        return new

    async def get_last_weather(self, search: Optional[str]) -> List[CityWeather]:
        if search:
            query = """
                SELECT cities.id, cities.name, cw.temperature, cw.pressure, cw.wind_speed, cw.datetime
                FROM cities
                INNER JOIN city_weathers AS cw
                    ON cw.city_id=cities.id
                    AND cw.datetime=(SELECT datetime FROM city_weathers AS cw1
                        WHERE cw1.city_id=cities.id
                        ORDER BY datetime DESC limit 1
                    )
                WHERE cities.name LIKE :search
            """
            values = {
                'search': search + '%'
            }
            return await self.database.fetch_all(query, values=values)
        query = """
            SELECT cities.id, cities.name, cw.temperature, cw.pressure, cw.wind_speed, cw.datetime
            FROM cities
            INNER JOIN city_weathers AS cw
                ON cw.city_id=cities.id
                AND cw.datetime=(SELECT datetime FROM city_weathers AS cw1
                    WHERE cw1.city_id=cities.id
                    ORDER BY datetime DESC limit 1
                )
        """
        return await self.database.fetch_all(query)

    async def get_statistics(self, city_name: str, date_start: datetime.date, date_end: datetime.date) -> WeatherStatistics:
        current_city = await self.get(city.c.name == city_name)
        if not current_city:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Город не добавлен')

        query = """
            SELECT cw.temperature, cw.pressure, cw.wind_speed, cw.datetime
            FROM cities
            INNER JOIN city_weathers AS cw
                ON cw.city_id=cities.id
            WHERE cities.id = :city_id AND datetime > :date_start AND datetime <= :date_end
        """
        values = {
            'city_id': current_city.id,
            'date_start': date_start,
            'date_end': date_end
        }
        statistics = await self.database.fetch_all(query, values=values)
        if len(statistics) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Статистика отсутствует')

        city_stat = []

        for statistic in statistics:
            city_stat.append(CityStatistics(
                temperature=statistic[0],
                pressure=statistic[1],
                wind_speed=statistic[2],
                datetime=statistic[3],
            ))

        avg = await self._avg_stat(current_city.id, date_start, date_end)

        weather_stat = WeatherStatistics(
            id=current_city.id,
            name=current_city.name,
            avg_temperature=avg.avg_temperature,
            avg_pressure=avg.avg_pressure,
            avg_wind_speed=avg.avg_wind_speed,
            statistics=city_stat
        )

        return weather_stat

    async def _avg_stat(self, city_id: int, date_start: datetime.date, date_end: datetime.date) -> AvgStat:
        query = """
            SELECT AVG(cw.temperature), AVG(cw.pressure), AVG(cw.wind_speed)
            FROM cities
            INNER JOIN city_weathers AS cw
            ON cw.city_id=cities.id
            WHERE cities.id = :city_id AND datetime > :date_start AND datetime <= :date_end
        """
        values = {
            'city_id': city_id,
            'date_start': date_start,
            'date_end': date_end
        }
        avg = await self.database.fetch_one(query, values=values)
        return AvgStat(
            avg_temperature=avg[0],
            avg_pressure=avg[1],
            avg_wind_speed=avg[2],
        )

