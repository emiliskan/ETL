from abc import ABCMeta, abstractmethod
from pydantic import BaseSettings, Field


class PostgreSettings(BaseSettings):
    """
    Настройки подключения к базе данных
    """
    dbname: str = Field(..., env='POSTGRES_DB')
    user: str = Field(..., env='POSTGRES_USER')
    password: str = Field(..., env='POSTGRES_PASSWORD')
    host: str = Field(..., env='POSTGRES_HOST')
    port: str = Field(..., env='POSTGRES_PORT')

    class Config:
        env_file: str = '.env'


class AbstractExtractor:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_data(self):
        """
        Возвращает массив не индексированных объектов
        :return:
        """

    @abstractmethod
    def set_index(self):
        """
        Выставляет загруженным объектам признак индексации
        :return:
        """


class AbstractTransformer:
    __metaclass__ = ABCMeta

    @abstractmethod
    def transform(self, row):
        """
        Преобразование строки в формат для загрузки
        :param row: объект для преобразования
        :return:
        """


class AbstractLoader:
    __metaclass__ = ABCMeta

    @abstractmethod
    def load(self, data):
        """
        Реализация этапа загрзки данных
        :param data: массив данных для загрузки
        :return:
        """
