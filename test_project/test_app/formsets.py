from fancy_formsets.forms import FancyBaseInlineFormSet

from models import Author, Book, Quote
from django.forms.models import inlineformset_factory

BookFormset = inlineformset_factory(
    Author, 
    Book,
    formset=FancyBaseInlineFormSet,
    extra=20
)

QuoteFormset = inlineformset_factory(
    Author, 
    Quote,
    formset=FancyBaseInlineFormSet,
    extra=20
)