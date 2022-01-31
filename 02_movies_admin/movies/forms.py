from django import forms

from dal import autocomplete

from .models import PersonFilmwork


class PersonAutocompleteForm(forms.ModelForm):
    class Meta:
        model = PersonFilmwork
        fields = ('__all__')
        widgets = {
            'person': autocomplete.ModelSelect2(url='person-autocomplete'),
        }
