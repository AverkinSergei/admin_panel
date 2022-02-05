import os
import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from postgres import PostgresSaver
from sqlite import SQLiteLoader
from tables import TABLES_MAP

BATCH_SIZE = 50


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn, tables_map=TABLES_MAP)
    sqlite_loader = SQLiteLoader(connection, batch_size=BATCH_SIZE)

    for table_name in TABLES_MAP:
        for data in sqlite_loader.load_movies(table_name=table_name):
            postgres_saver.save_all_data(data)


if __name__ == '__main__':
    dsn = {'dbname': os.environ.get('DB_NAME'),
           'user': os.environ.get('DB_USER'),
           'password': os.environ.get('DB_PASSWORD'),
           'host': os.environ.get('DB_HOST'),
           'port': os.environ.get('DB_PORT')}
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(
            **dsn, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)

    sqlite_conn.close()
    pg_conn.close()
