from crispy_forms.helper import FormHelper


class InlineFormHelper(FormHelper):
    pass


class InlineFormsetHelper(FormHelper):
    template_name = 'fancy_formsets_bootstrap/formset.html'
