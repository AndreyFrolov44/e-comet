import json
import urllib

import psycopg2
import scrapy

from openweathermap.settings import POSTGRES_HOST, POSTGRES_USER, POSTGRES_DB, POSTGRES_PASSWORD
from openweathermap.items import OpenweathermapItem


class WeatherSpider(scrapy.Spider):
    name = "weather"
    BASE_URL = 'https://openweathermap.org/data/2.5/onecall'
    # start_urls = ['https://openweathermap.org/data/2.5/onecall?lat=51.5085&lon=-0.1257&units=metric&appid=439d4b804bc8187953eb36d2a8c26a02']

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en - US, en; q = 0.9, ru - RU; q = 0.8, ru; q = 0.7, uk; q = 0.6',
        'Connection': 'keep-alive',
        'Host': 'openweathermap.org',
        'Referer': 'https://openweathermap.org/',
        'sec-ch-ua': '"Not_A Brand"; v = "99", "Google Chrome"; v = "109", "Chromium"; v = "109"',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }

    def start_requests(self):
        connection = psycopg2.connect(host=POSTGRES_HOST, user=POSTGRES_USER, password=POSTGRES_PASSWORD,
                                      dbname=POSTGRES_DB)
        cur = connection.cursor()

        cur.execute("""
            SELECT id, name, lat, lon FROM cities
        """)
        cities = cur.fetchall()

        params = {
            'units': 'metric',
            'appid': '439d4b804bc8187953eb36d2a8c26a02'
        }

        for city in cities:
            params['lat'] = city[2]
            params['lon'] = city[3]
            yield scrapy.Request(
                url=f'{self.BASE_URL}?{urllib.parse.urlencode(params)}',
                callback=self.parse_temp,
                meta={'id': city[0]}
            )

    def parse_temp(self, response):
        weather_item = OpenweathermapItem()
        weather_item['id'] = response.meta.get('id')
        weather_item['temperature'] = json.loads(response.body)['current']['temp']
        weather_item['pressure'] = json.loads(response.body)['current']['pressure']
        weather_item['wind_speed'] = json.loads(response.body)['current']['wind_speed']
        yield weather_item




