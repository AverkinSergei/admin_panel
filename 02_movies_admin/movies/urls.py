from django.urls import path

from .views import PersonAutocomplete


urlpatterns = [
    path('person-autocomplete/', PersonAutocomplete.as_view(), name='person-autocomplete'),
]
