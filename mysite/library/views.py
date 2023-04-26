from django.shortcuts import render
from django.http import HttpResponse

from .models import Book, BookInstance, Author

# Create your views here.

# cia backendo darbas

def index(request):
    # return HttpResponse("Labas, pasauli!")
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_authors = Author.objects.count()

    # filtruojam available knygas
    num_instances_available = BookInstance.objects.filter(status__exact='g').count()

    #sudedam visus i masyva:
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_authors': num_authors,
        'num_instances_available': num_instances_available,
    }

    return render(request, 'index.html', context=context)

# dabar frontend'as: