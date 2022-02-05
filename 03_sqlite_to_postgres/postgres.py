from psycopg2.extras import execute_values


class PostgresSaver(object):

    def __init__(self, pg_conn, tables_map):
        self.connection = pg_conn
        self.tables_map = tables_map

    def save_all_data(self, data):
        with self.connection.cursor() as cursor:
            for table_name in data:
                slots = self.tables_map[table_name].__slots__
                columns = tuple(sorted(slots))
                query = f'INSERT INTO content.{table_name} {columns} VALUES'
                query = query.replace('\'', '')
                values = data[table_name]
                if values:
                    execute_values(
                        cursor,
                        f'{query} %s ON CONFLICT (id) DO NOTHING;', values)
