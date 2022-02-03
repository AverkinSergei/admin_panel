import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

    def __str__(self):
        return self.name


class Filmwork(UUIDMixin, TimeStampedMixin):

    class FilmType(models.TextChoices):
        MOVIE = 'movie'
        TV_SHOW = 'tv_show'

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation date'))
    rating = models.SmallIntegerField(
        _('rating'), blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)])
    type = models.CharField(
        _('type'), max_length=20,
        choices=FilmType.choices, default=FilmType.MOVIE)
    genres = models.ManyToManyField(
        Genre, through='GenreFilmwork', verbose_name=_('genres'))
    certificate = models.CharField(
        _('certificate'), max_length=512, null=True, blank=True)
    file_path = models.FileField(
        _('file'), blank=True, null=True, upload_to='movies/')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('filmwork')
        verbose_name_plural = _('filmworks')

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey(
        'Genre', on_delete=models.CASCADE, verbose_name=_('genre'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        unique_together = ('film_work', 'genre')


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full name'), max_length=255)
    birth_date = models.DateField(_('birth_date'), null=True, blank=True)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('person')
        verbose_name_plural = _('persons')

    def __str__(self):
        return self.full_name


class PersonFilmwork(models.Model):
    film_work = models.ForeignKey(
        'Filmwork', on_delete=models.CASCADE, verbose_name=_('filmwork'))
    person = models.ForeignKey(
        'Person', on_delete=models.CASCADE, verbose_name=_('person'))
    role = models.TextField(_('role'), null=True)
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
