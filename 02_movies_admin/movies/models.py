import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField('название', max_length=255)
    description = models.TextField('описание', blank=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.name


class Filmwork(UUIDMixin, TimeStampedMixin):

    class FilmType(models.TextChoices):
        MOVIE = 'movie'
        TV_SHOW = 'tv_show'

    title = models.CharField('название', max_length=255)
    description = models.TextField('описание', blank=True)
    creation_date = models.DateTimeField('дата создания')
    rating = models.SmallIntegerField('рейтинг', blank=True,
                                      validators=[MinValueValidator(0),
                                                  MaxValueValidator(100)])
    type = models.CharField('тип', max_length=20, choices=FilmType.choices, default=FilmType.MOVIE)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = 'кинопроизведение'
        verbose_name_plural = 'кинопроизведения'

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField('полное имя', max_length=255)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = 'участник фильма'
        verbose_name_plural = 'участники фильма'

    def __str__(self):
        return self.full_name


class PersonFilmwork(models.Model):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField('роль', null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
