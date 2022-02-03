from tests import movies_dataclasses


class SQLiteLoader(object):

    def __init__(self, connection):
        self.connection = connection

    def load_movies(self):
        return {
            'film_work': [
                movies_dataclasses.Filmwork(*row)
                for row in self.connection.execute('select * from film_work')
            ],
            'person': [
                movies_dataclasses.Person(*row)
                for row in self.connection.execute('select * from person')
            ],
            'genre': [
                movies_dataclasses.Genre(*row)
                for row in self.connection.execute('select * from genre')
            ],
            'genre_film_work': [
                movies_dataclasses.GenreFilmwork(*row)
                for row in self.connection.execute(
                    'select * from genre_film_work')
            ],
            'person_film_work': [
                movies_dataclasses.PersonFilmwork(*row)
                for row in self.connection.execute(
                    'select * from person_film_work')
            ],
        }
