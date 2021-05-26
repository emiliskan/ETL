import logging
from typing import List
import requests
import json
from urllib.parse import urljoin
from models import AbstractLoader

logger = logging.getLogger()


class ESLoader(AbstractLoader):
    def __init__(self, url: str):
        self.url = url

    def load(self, data):
        self.load_to_es(data, 'movies')

    def _get_es_bulk_query(self, rows: List[dict], index_name: str) -> List[str]:
        """
        Подготавливает bulk-запрос в Elasticsearch
        """
        prepared_query = []
        for row in rows:
            prepared_query.extend([
                json.dumps({'index': {'_index': index_name, '_id': row['id']}}),
                json.dumps(row)
            ])
        return prepared_query

    def load_to_es(self, records: List[dict], index_name: str):
        """
        Отправка запроса в ES и разбор ошибок сохранения данных
        """
        prepared_query = self._get_es_bulk_query(records, index_name)
        str_query = '\n'.join(prepared_query) + '\n'

        response = requests.post(
            urljoin(self.url, '_bulk'),
            data=str_query,
            headers={'Content-Type': 'application/x-ndjson'}
        )

        json_response = json.loads(response.content.decode())
        for item in json_response['items']:
            error_message = item['index'].get('error')
            if error_message:
                logger.error(error_message)
