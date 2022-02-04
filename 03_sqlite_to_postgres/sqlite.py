from tests import movies_dataclasses


class SQLiteLoader(object):

    def __init__(self, connection, batch_size=50):
        self.connection = connection
        self.batch_size = batch_size

    def load_movies(self, table_name):
        return {
            'film_work': [
                movies_dataclasses.Filmwork(*row)
                for row in self.connection.cursor().execute(
                    'select * from film_work').fetchmany(self.batch_size)
            ],
            'person': [
                movies_dataclasses.Person(*row)
                for row in self.connection.cursor().execute(
                    'select * from person').fetchmany(self.batch_size)
            ],
            'genre': [
                movies_dataclasses.Genre(*row)
                for row in self.connection.cursor().execute(
                    'select * from genre').fetchmany(self.batch_size)
            ],
            'genre_film_work': [
                movies_dataclasses.GenreFilmwork(*row)
                for row in self.connection.cursor().execute(
                    'select * from genre_film_work').fetchmany(self.batch_size)
            ],
            'person_film_work': [
                movies_dataclasses.PersonFilmwork(*row)
                for row in self.connection.cursor().execute(
                    'select * from person_film_work').fetchmany(
                    self.batch_size)
            ],
        }
