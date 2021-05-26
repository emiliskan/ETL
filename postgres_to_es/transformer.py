from models import AbstractTransformer


class Transformer(AbstractTransformer):

    def transform(self, row) -> dict:
        """
        Преобразование названий полей в структуру для elastic search

        :param row: поле для преобразования
        :return:
        """

        return {
                'id': row['id'],
                'title': row['title'],
                'description': row['description'],
                'imdb_rating': row['rating'],
                'genre': row['genres'],
                'writers': row['writers'],
                'actors': row['actors'],
                'directors': row['directors'],
            }
