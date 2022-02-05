import os
import argparse
import psycopg2
import sqlite3
from datetime import datetime
from psycopg2.extras import DictCursor

import movies_dataclasses as md


parser = argparse.ArgumentParser()

parser.add_argument(
    '-p', '--postgresql',
    required=False,
    help='Путь к БД PostgreSQL, example: username:password@localhost:5432')
parser.add_argument(
    '-s', '--sqlite',
    required=False,
    help='Путь к БД SQLite, example: /home/user/db.sqlite')

args = vars(parser.parse_args())

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

postgresql_arg = args.get(
    'postresql', f'{DB_USER}:{DB_PASSWORD}@127.0.0.1:5432')
postgresql_cred, postgresql_path = postgresql_arg.split('@')
postgresql_user, postgresql_password = postgresql_cred.split(':')
postgresql_host, postgresql_port = postgresql_path.split(':')

sqlite = args.get('sqlite', 'db.sqlite')


with psycopg2.connect(
        dbname='movies_database',
        user=postgresql_user,
        password=postgresql_password,
        host=postgresql_host,
        port=postgresql_port,
        cursor_factory=DictCursor) as pg_conn, sqlite3.connect(
        sqlite) as sqlite_conn:

    table_map = {
        'film_work': md.Filmwork,
        'genre': md.Genre,
        'person': md.Person,
        'genre_film_work': md.GenreFilmwork,
        'person_film_work': md.PersonFilmwork,
    }
    for table_name in table_map:
        pg_columns = ', '.join(table_map[table_name].__slots__)
        sqlite_columns = pg_columns.replace('created', 'created_at')
        sqlite_columns = sqlite_columns.replace('modified', 'updated_at')
        with pg_conn.cursor() as cursor:
            cursor.execute(f'SELECT {pg_columns} FROM content.{table_name};')
            pg_data = cursor.fetchall()
        sqlite_data = sqlite_conn.execute(
            f'SELECT {sqlite_columns} FROM {table_name};').fetchall()
        assert len(pg_data) == len(sqlite_data)
        for idx in range(len(pg_data)):
            pg_obj = table_map[table_name](*pg_data[idx])
            sqlite_obj = table_map[table_name](*sqlite_data[idx])
            for field in pg_obj.__slots__:
                if field in ('created', 'modified'):
                    pg_dt = getattr(pg_obj, field)
                    sqlite_dt = datetime.strptime(
                        f'{getattr(sqlite_obj, field)}00',
                        '%Y-%m-%d %H:%M:%S.%f%z')
                    assert pg_dt == sqlite_dt
                else:
                    assert getattr(pg_obj, field) == getattr(sqlite_obj, field)
    print('check done!')
