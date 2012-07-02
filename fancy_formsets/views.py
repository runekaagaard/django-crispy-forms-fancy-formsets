# coding=utf-8
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.forms.formsets import DELETION_FIELD_NAME

from crispy_forms.layout import Submit
from fancy_formsets.helper import InlineFormHelper, InlineFormsetHelper


class FormsetsView(TemplateView):
    formsets = {}
    inputs = [Submit('submit', _('Save changes'), css_class='btn-primary')]
    message_on_save = _("The changes was succesfully saved.")
    readonly = False

    def is_valid(self, context):
        return not any(map(lambda x: not x.is_valid(), context['formsets']))

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if (self.is_valid(context)):
            map(lambda x: x.save(), context['formsets'])
            messages.add_message(request, messages.SUCCESS,
                                 self.message_on_save)

            return HttpResponseRedirect("")

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(FormsetsView, self).get_context_data(**kwargs)
        context['formsets'] = []
        for formset_setting in self.formset_settings:
            formset = formset_setting['class'](
                instance=formset_setting['get_instance'](self),
                data=self.request.POST or None
            )
            formset.readonly = self.readonly
            if not hasattr(formset.form, "helper"):
                formset.form.helper = InlineFormHelper()
            if not hasattr(formset, "helper"):
                formset.helper = InlineFormsetHelper()

            for form in formset.forms:
                matrix = (form in formset.extra_forms, form.is_bound,
                          DELETION_FIELD_NAME in form.changed_data)
                form.is_extra = matrix in ((True, False, True),
                                           (True, True, False))
            formset.settings = formset_setting
            context['formsets'].append(formset)

        if not self.readonly:
            context['formsets_inputs'] = self.inputs

        return context
