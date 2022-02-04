from django.contrib import admin

from .forms import PersonAutocompleteForm
from .models import Genre, Filmwork, Person, GenreFilmwork, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', )


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    form = PersonAutocompleteForm


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline, )
    list_display = ('title', 'type', 'creation_date', 'rating', )
    list_filter = ('type', 'creation_date', )
    search_fields = ('title', 'description', 'id', )

    def get_queryset(self, request, **kwargs):
        qs = super().get_queryset(request)
        return qs.prefetch_related('genres')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (PersonFilmworkInline, )
    list_display = ('full_name', )
