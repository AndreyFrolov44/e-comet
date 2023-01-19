import psycopg2

from openweathermap.settings import POSTGRES_HOST, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB


class OpenweathermapPipeline:
    def __init__(self):
        self.connection = psycopg2.connect(host=POSTGRES_HOST, user=POSTGRES_USER, password=POSTGRES_PASSWORD,
                                           dbname=POSTGRES_DB)
        self.cur = self.connection.cursor()

    def process_item(self, item, spider):
        self.cur.execute(""" INSERT INTO city_weathers (city_id, temperature, pressure, wind_speed) VALUES (%s,%s,%s,%s)""", (
            item["id"],
            item["temperature"],
            item["pressure"],
            item["wind_speed"],
        ))
        self.connection.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()
