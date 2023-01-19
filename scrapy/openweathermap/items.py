# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class OpenweathermapItem(scrapy.Item):
    id = Field()
    temperature = Field()
    pressure = Field()
    wind_speed = Field()
