from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=80)
    
class Book(models.Model):
    author = models.ForeignKey(Author)
    year = models.IntegerField()
    title = models.CharField(max_length=80)
    
    class Meta():
        verbose_name = "Book"
        verbose_name_plural = "Books"
    
class Quote(models.Model):
    author = models.ForeignKey(Author)
    date = models.DateField()
    quote = models.TextField()
    
    class Meta():
        verbose_name = "Quote"
        verbose_name_plural = "Quotes"