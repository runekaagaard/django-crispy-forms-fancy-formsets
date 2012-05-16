# -*- coding: utf-8 -*-
from django.conf import settings
from django.forms.formsets import BaseFormSet, DELETION_FIELD_NAME
from django.template import Context
from django.template.loader import get_template
from django import template

from crispy_forms.helper import FormHelper
from crispy_forms.templatetags.crispy_forms_tags import BasicNode

from fancy_formsets.widgets import ReadOnlyWidget
from django.template.base import Variable

register = template.Library()
       
class FancyFormsetsNode(BasicNode):
    def render(self, context):
        helper = self.helper.resolve(context)
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

from django import template
import datetime

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
            
        try: bound_field.field.widget.queryset = bound_field.field.queryset
        except AttributeError: pass
        
        return bound_field
        
@register.tag()
def fancy_formsets_field_readonly(parser, token):
    token = token.split_contents()
    field_name = token.pop(1)
    return ReadonlyFieldNode(field_name)
