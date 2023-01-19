import json
import os

import scrapy

from core.config import PATH


class WeatherSpider(scrapy.Spider):
    name = "city"

    custom_settings = {
        'FEEDS': {'city.json': {'format': 'json', }}
    }

    def __init__(self, city=None, *args, **kwargs):
        super(WeatherSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'https://openweathermap.org/data/2.5/find?q={city}&appid=439d4b804bc8187953eb36d2a8c26a02&units=metric']

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

    def parse(self, response):
        data = json.loads(response.body)
        # try:
        #     city_id = data['list'][0]['id']
        #     city_lat = data['list'][0]['id']
        # except IndexError:
        #     city_id = None
        yield {
            'id': data['list'][0]['id'] if data['count'] > 0 else None,
            'lat': data['list'][0]['coord']['lat'] if data['count'] > 0 else None,
            'lon': data['list'][0]['coord']['lon'] if data['count'] > 0 else None
        }
