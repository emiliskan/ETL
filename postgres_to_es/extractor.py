import logging
from psycopg2.extensions import connection as _connection
from psycopg2.extras import RealDictCursor
from models import AbstractExtractor

logger = logging.getLogger()


class PostgresExtractor(AbstractExtractor):

    data = []

    def __init__(self, pg_conn: _connection):
        self.conn = pg_conn
        self.cursor = pg_conn.cursor(cursor_factory=RealDictCursor)

    def get_data(self):
        """
        Получает не проиндексированные фильмы с сопутствующими данными
        :return: результат выборки
        """
        sql = """
            WITH movies AS (
                SELECT
                    id, 
                    title, 
                    description, 
                    rating, 
                    type 
                FROM movies_media
                WHERE not indexed
                LIMIT 100
            )
            SELECT
                fw.id, 
                fw.title, 
                fw.description, 
                fw.rating, 
                fw.type,
                CASE
                    WHEN pfw.person_type = 'actor' 
                    THEN ARRAY_AGG(distinct p.first_name || ' ' || p.last_name)
                END AS actors,
                CASE
                    WHEN pfw.person_type = 'writer' 
                    THEN ARRAY_AGG(distinct p.first_name || ' ' || p.last_name)
                END AS writers,
                CASE
                    WHEN pfw.person_type = 'director' 
                    THEN ARRAY_AGG(distinct p.first_name || ' ' || p.last_name)
                END AS directors,
                ARRAY_AGG(g.name) AS genres
            FROM movies as fw
            LEFT JOIN movies_personmedia pfw ON pfw.film_id = fw.id
            LEFT JOIN movies_person p ON p.id = pfw.person_id
            LEFT JOIN movies_genremedia gfw ON gfw.film_id = fw.id
            LEFT JOIN movies_genre g ON g.id = gfw.genre_id
            GROUP BY
                fw.id, 
                fw.title, 
                fw.description, 
                fw.rating, 
                fw.type, 
                pfw.person_type	                   
        """

        self.cursor.execute(sql)
        self.data = self.cursor.fetchall()

        logger.info("Extracted", len(self.data))
        return self.data

    def set_index(self):
        """
        После загрузки устанавливается признак индексации
        Снятие индексации происходит во время обновления записей в админке
        :return:
        """
        data = ','.join(self.cursor.mogrify("%s", (item["id"],)).decode()
                        for item in self.data)
        sql = f"""
            UPDATE content.movies_media
            SET indexed = True
            WHERE id in ({data});
        """

        self.cursor.execute(sql, (data, ))
        self.conn.commit()
        logger.info("Indexed")
