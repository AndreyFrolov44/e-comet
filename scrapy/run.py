import os
import time

if __name__ == "__main__":
    while True:
        os.system('scrapy crawl weather')
        time.sleep(60)
