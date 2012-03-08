# Create your views here.
from fancy_formsets.views import FormsetsView
from models import Author, Book, Quote
from formsets import BookFormset, QuoteFormset
from django.shortcuts import get_object_or_404

class Edit(FormsetsView):
    template_name = 'test_app/edit.html'

    formset_settings = (
        {
            'class': BookFormset,
            'get_instance': lambda self: self.author,
        },
        {
            'class': QuoteFormset,
            'get_instance': lambda self: self.author,
        },
    )

    def __init__(self, *args, **kwargs):
        super(Edit, self).__init__(*args, **kwargs)
    
    def init(self, request, author_id):
        self.author = get_object_or_404(Author, pk=author_id)
    
    def get(self, request, author_id=None, *args, **kwargs):
        self.init(request, author_id)
        return super(Edit, self).get(request, author_id=author_id, 
                                     *args, **kwargs)
    
    def post(self, request, author_id=None, *args, **kwargs):
        self.init(request, author_id)
        return super(Edit, self).post(request, author_id=author_id, 
                                      *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(Edit, self).get_context_data(**kwargs)
        
        context.update({
            'author': self.author,
            'request': self.request,
        })
        return context