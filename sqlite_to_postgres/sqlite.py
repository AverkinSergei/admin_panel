from tables import TABLES_MAP


class SQLiteLoader(object):
    def __init__(self, connection, batch_size=50):
        self.connection = connection
        self.batch_size = batch_size

    def load_movies(self, table_name):
        columns = ', '.join(sorted(
            TABLES_MAP[table_name].__slots__)).replace(
            'created', 'created_at').replace('modified', 'updated_at')
        cur = self.connection.cursor().execute(
            f'select {columns} from {table_name}')
        rows = cur.fetchmany(self.batch_size)
        while rows:
            yield {table_name: rows}
            rows = cur.fetchmany(self.batch_size)
