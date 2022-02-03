import uuid
from datetime import date, datetime
from dataclasses import dataclass


@dataclass
class BaseDataClass(object):
    id: uuid.UUID
    created: datetime


class DataClass(BaseDataClass):
    modified: datetime


class Filmwork(DataClass):
    __slots__ = ['id', 'title', 'description', 'creation_date',
                 'certificate', 'file_path', 'rating', 'type',
                 'created', 'modified']
    title: str
    description: str
    creation_date: date
    certificate: str
    file_path: str
    rating: float
    type: str

    def __init__(self, id, title, description, creation_date,
                 certificate, file_path, rating, type,
                 created, modified):
        self.id = id
        self.title = title
        self.description = description
        self.creation_date = creation_date
        self.certificate = certificate
        self.file_path = file_path
        self.rating = rating
        self.type = type
        self.created = created
        self.modified = modified


class Person(DataClass):
    __slots__ = ['id', 'full_name', 'birth_date', 'created', 'modified']
    full_name: str
    birth_date: date

    def __init__(self, id, full_name, birth_date, created, modified):
        self.id = id
        self.full_name = full_name
        self.birth_date = birth_date
        self.created = created
        self.modified = modified


class Genre(DataClass):
    __slots__ = ['id', 'name', 'description', 'created', 'modified']
    name: str
    description: str

    def __init__(self, id, name, description, created, modified):
        self.id = id
        self.name = name
        self.description = description
        self.created = created
        self.modified = modified


class GenreFilmwork(BaseDataClass):
    __slots__ = ['id', 'film_work_id', 'genre_id', 'created']
    film_work_id: uuid.UUID
    genre_id: uuid.UUID

    def __init__(self, id, film_work_id, genre_id, created):
        self.id = id
        self.film_work_id = film_work_id
        self.genre_id = genre_id
        self.created = created


class PersonFilmwork(BaseDataClass):
    __slots__ = ['id', 'film_work_id', 'person_id', 'role', 'created']
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str

    def __init__(self, id, film_work_id, person_id, role, created):
        self.id = id
        self.film_work_id = film_work_id
        self.person_id = person_id
        self.role = role
        self.created = created
