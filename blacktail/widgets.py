import json
from django.forms import widgets
from . import models


class AuthorsWidget(widgets.SelectMultiple):

    def __init__(self, attrs=None, choices=()):
        authors = [(a.pk, a.name) for a in models.Author.objects.all()]
        super().__init__(attrs, authors)

    def format_value(self, value):
        return json.loads(value)

    def value_from_datadict(self, data, files, name):
        rv = super().value_from_datadict(data, files, name)
        return [int(v) for v in rv]

    def optgroups(self, name, value, attrs=None):
        options = list(super().optgroups(name, [str(v) for v in value], attrs))
        by_value = {i[1][0]['value']: i for i in options}
        return (
            [i for i in options if i[1][0]['value'] not in value] +
            [by_value[v] for v in value]
        )
