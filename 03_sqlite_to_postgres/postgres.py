class PostgresSaver(object):

    def __init__(self, pg_conn, batch_size):
        self.connection = pg_conn
        self.batch_size = batch_size

    @staticmethod
    def mogrify(cursor, obj):
        return cursor.mogrify(
            '({0})'.format(', '.join(
                ['%s' for _ in range(len(obj.__slots__))])),
            tuple(getattr(obj, name)
                  for name in sorted(obj.__slots__))
        ).decode()

    def save_all_data(self, data):
        with self.connection.cursor() as cursor:
            for table_name in data:
                columns = tuple(sorted(data[table_name][0].__slots__))
                query = f'INSERT INTO content.{table_name} {columns} VALUES '
                query = query.replace('\'', '')
                start = 0
                end = self.batch_size
                steps = len(data[table_name]) // self.batch_size + 1
                for step in range(steps):
                    values = ', '.join([
                        self.mogrify(cursor, obj)
                        for obj in data[table_name][start:end]
                    ])
                    if values:
                        cursor.execute(
                            f'{query}{values} ON CONFLICT (id) DO NOTHING;')
                    start = end
                    end += self.batch_size
