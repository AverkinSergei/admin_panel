import os
import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from tests import movies_dataclasses as md
from sqlite import SQLiteLoader
from postgres import PostgresSaver


TABLES_MAP = {
    'film_work': md.Filmwork,
    'genre': md.Genre,
    'person': md.Person,
    'genre_film_work': md.GenreFilmwork,
    'person_film_work': md.PersonFilmwork,
}

BATCH_SIZE = 50


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn, batch_size=BATCH_SIZE)
    sqlite_loader = SQLiteLoader(connection, batch_size=BATCH_SIZE)

    for table_name in TABLES_MAP:
        data = sqlite_loader.load_movies(table_name=table_name)
        postgres_saver.save_all_data(data)


if __name__ == '__main__':
    dsl = {'dbname': os.environ.get('DB_NAME'),
           'user': os.environ.get('DB_USER'),
           'password': os.environ.get('DB_PASSWORD'),
           'host': os.environ.get('DB_HOST'),
           'port': os.environ.get('DB_PORT')}
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(
            **dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)

    sqlite_conn.close()
    pg_conn.close()
