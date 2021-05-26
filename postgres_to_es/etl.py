from time import sleep
from functools import wraps
import os
import psycopg2

from extractor import PostgresExtractor
from loader import ESLoader
from transformer import Transformer

from models import AbstractExtractor, AbstractLoader, AbstractTransformer


def coroutine(func):
    @wraps(func)
    def inner(*args, **kwargs):
        fn = func(*args, **kwargs)
        next(fn)
        return fn

    return inner


def etl(target):
    while True:
        target.send(1)
        sleep(0.1)


@coroutine
def extract(target, extractor: AbstractExtractor):
    """ Получение неиндексированных фильмов """
    while _ := (yield):

        data = extractor.get_data()
        data_count = len(data)
        if data_count == 0:
            continue

        target.send(data)
        extractor.set_index()


@coroutine
def transform(target, transformer: AbstractTransformer):
    """ Подготовка записей для загрузки в elastic """
    while result := (yield):
        transformed = []
        for row in result:
            transformed.append(transformer.transform(row))

        target.send(transformed)


@coroutine
def load(loader: AbstractLoader):
    """ Загрузка в elastic """
    while data := (yield):
        if len(data) == 0:
            continue

        loader.load(data)
        print("Loaded!")


if __name__ == '__main__':
    dsl = {
        'dbname': os.getenv('POSTGRES_DB'),
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'host': os.getenv('POSTGRES_HOST'),
        'port': os.getenv('POSTGRES_PORT'),
    }

    with psycopg2.connect(**dsl) as pg_conn:

        # этап загрузки в es
        loader = load(ESLoader(os.getenv("ES_HOST")))

        # этап подготовки данных
        transformer = transform(loader, Transformer())

        # этап получения записей
        extractor = extract(transformer, PostgresExtractor(pg_conn))

        # запуск etl процесса
        etl(extractor)


#TODO: backoff, insert search schema, check search working