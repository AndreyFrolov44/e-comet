import os


def run_city(city: str) -> None:
    os.system(f'scrapy crawl city -a city={city}')