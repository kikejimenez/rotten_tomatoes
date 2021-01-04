# Rotten_tomatoes

Rotten tomatoes scraper and database

## Scrapper

### Docker

Build image

```shell
docker build -t selenium_py3 .
```

Run container

```shell
docker run --rm -it  -v $PWD:/wd -w /wd -v /dev/shm:/dev/shm -p 5000:5000 selenium_py3 bash
```

Run script inside src folder

## Oracle Database

### Docker-compose

Run

```shell
docker-compose up
```


