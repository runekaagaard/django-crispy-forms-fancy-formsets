# -*- coding: utf-8 -*-
from django.forms.formsets import DELETION_FIELD_NAME
from django.template.loader import get_template
from django import template

from crispy_forms.templatetags.crispy_forms_tags import BasicNode

from fancy_formsets.widgets import ReadOnlyWidget
from django.template.base import Variable

register = template.Library()


class FancyFormsetsNode(BasicNode):
    def render(self, context):
        if self not in context.render_context:
            context.render_context[self] = (
                Variable(self.form),
                Variable(self.helper) if self.helper else None
            )
        form, helper = context.render_context[self]
        actual_form = form.resolve(context)
        if self.helper is not None:
            helper = helper.resolve(context)
        else:
            helper = actual_form.helper
        template = get_template(helper.template_name)
        c = self.get_render(context)
        return template.render(c)


# {% fancy_formsets %} tag
@register.tag(name="fancy_formsets")
def do_fancy_formsets(parser, token):
    token = token.split_contents()
    form = token.pop(1)

    try:
        helper = token.pop(1)
    except IndexError:
        helper = None
    return FancyFormsetsNode(form, helper)


class ReadonlyFieldNode(template.Node):
    def __init__(self, field_name):
        self.field_name = field_name

    def render(self, context):
        bound_field = context[self.field_name]
        if bound_field.name == DELETION_FIELD_NAME:
            return ""
        # If the widget implements the render_readonly() method, use that
        # instead of the render() method.
        if hasattr(bound_field.field.widget, "render_readonly"):
            bound_field.field.widget.render = \
                bound_field.field.widget.render_readonly
        else:
            bound_field.field.widget = ReadOnlyWidget()

        try:
            bound_field.field.widget.queryset = bound_field.field.queryset
        except AttributeError:
            pass

        return bound_field


@register.tag()
def fancy_formsets_field_readonly(parser, token):
    token = token.split_contents()
    field_name = token.pop(1)
    return ReadonlyFieldNode(field_name)
