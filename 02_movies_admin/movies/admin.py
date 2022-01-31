from django.contrib import admin
from .models import Genre, Filmwork, Person, GenreFilmwork, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', )


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, )
    list_display = ('title', 'type', 'creation_date', 'rating', )
    list_filter = ('type', 'creation_date', )
    search_fields = ('title', 'description', 'id', )


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (PersonFilmworkInline, )
    list_display = ('full_name', )
