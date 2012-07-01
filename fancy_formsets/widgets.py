# coding=utf-8

from django import forms
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode


class ReadOnlyWidget(forms.Select):
    """
    Widget that tries to display all model fields as readonly. Its a mix of
    HiddenInput and Select widget.
    """

    queryset = None

    def render(self, name, value, attrs=None, choices=()):
        def value_from_choices(choices, value):
            try:
                return dict(choices)[int(value)]
            except (KeyError, ValueError, TypeError):
                return value

        def value_from_queryset(queryset, value):
            if not value:
                return value
            return queryset.get(pk=value)

        if value is None:
            value = ''

        if choices:
            value = value_from_choices(choices, value)
        elif self.queryset:
            value = value_from_queryset(self.queryset, value)

        return mark_safe(force_unicode(value))
