from dal import autocomplete

from .models import Person


class PersonAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_staff:
            return Person.objects.none()

        qs = Person.objects.all()

        if self.q:
            qs = qs.filter(full_name__icontains=self.q)

        return qs
