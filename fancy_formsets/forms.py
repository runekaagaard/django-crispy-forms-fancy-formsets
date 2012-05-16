from django.forms.models import BaseInlineFormSet
from fancy_formsets.helper import InlineFormHelper, InlineFormsetHelper
from crispy_forms.templatetags.crispy_forms_tags import UniFormNode
from django.template.loader import get_template
from django.template.context import Context
from django.utils.html import escape
from django.forms.formsets import DELETION_FIELD_NAME

class FancyBaseInlineFormSet(BaseInlineFormSet):
    helper = None
    empty_form = None
    
    def __init__(self, *args, **kwargs):
        if not self.helper:
            self.helper = InlineFormsetHelper()
        self.verbose_name = self.model._meta.verbose_name
        self.verbose_name_plural = self.model._meta.verbose_name_plural
        self.model_name = str(self.model._meta).split(".")[-1]
        super(FancyBaseInlineFormSet, self).__init__(*args, **kwargs)
        self.empty_form = self._construct_form(9999999999999)
        for form in self.forms:
            if form in self.extra_forms:
                form.is_extra = True
                if self.can_delete:
                    form.fields[DELETION_FIELD_NAME].initial = True
            else:
                form.is_extra = False
        
    template = get_template("fancy_formsets_bootstrap/form.html")    
    def render_empty_form(self):
        self.empty_form.helper = InlineFormHelper()
        return escape(self.template.render(Context({"form": self.empty_form})))
