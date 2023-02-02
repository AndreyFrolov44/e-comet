# Тестовое задание e-comet

## Технологии
 - Python
 - FastApi
 - Postgres
 - Scrapy

## API

1. POST /weather/&lt;Название города&gt;/

Добавление в базу данных нового города. Если город уже существует, или он не найден на openweathermap, возникнет ошибка
#### Пример запроса
```
curl -X 'POST' \
  'http://localhost:8000/cities/weather/samara' \
  -H 'accept: application/json' \
  -d ''
```

#### Пример ответа
```json
{
  "id": 499068,
  "name": "samara",
  "lat": 53,
  "lon": 50
}
```

2. GET /last_weather/

Добавление в базу данных нового города. Если город уже существует, или он не найден на openweathermap, возникнет ошибка
#### Пример запроса
```
curl -X 'GET' \
  'http://localhost:8000/cities/last_weather?search=mo' \
  -H 'accept: application/json'
```

#### Пример ответа
```json
[
  {
    "id": 524901,
    "name": "moscow",
    "temperature": 1,
    "pressure": 1018,
    "wind_speed": 5.27,
    "datetime": "2023-01-19T16:29:56.890018"
  },
  {
    "id": 3116057,
    "name": "mos",
    "temperature": 11,
    "pressure": 1015,
    "wind_speed": 4.02,
    "datetime": "2023-01-19T16:29:56.676651"
  }
]
```

3. GET /city_stats/

Получает по заданному городу (передается query параметром) все данные за выбранный период, а также их средние значения за этот период.
#### Пример запроса
```
curl -X 'GET' \
  'http://localhost:8000/cities/city_stats?city=moscow&date_start=2023-01-18&date_end=2023-01-19' \
  -H 'accept: application/json'
```

#### Пример ответа
```json
{
  "avg_temperature": 1,
  "avg_pressure": 1015,
  "avg_wind_speed": 7.89,
  "id": 524901,
  "name": "moscow",
  "statistic": [
    {
      "temperature": 1,
      "pressure": 1015,
      "wind_speed": 7.77,
      "datetime": "2023-01-18T21:37:04.808867"
    },
    {
      "temperature": 1,
      "pressure": 1015,
      "wind_speed": 8.01,
      "datetime": "2023-01-18T23:02:30.122561"
    }
  ]
}
```

## Запуск
**Перед запуском необходимо заполнить файл ```.env```**

```shell
docker-compose up -d --build
```

При первом запуске также необходимо применить миграции
```
docker exec api-ecomet alembic upgrade head
```
