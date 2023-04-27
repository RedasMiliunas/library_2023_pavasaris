from django.shortcuts import render, get_object_or_404
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

# dabar frontend'as.

# django V - views.
# Views: gali buti function-base (kaip virsuje) arba
# class-base (daugiau django pasirinkimas - supaprastina darba): kuriam funkcija arba klase views.py faile!!
# galim juos miksuoti, taikyti pagal tai kas patogiau kuriam veiksmui atlikti.
# class-base: jeigu lendam giliau, reikia kazka keisti, tuomet reikes daryti komplikuociau - daryti overwrite'us klases metodams ir pan.

def authors(request):
    authors = Author.objects.all()
    context = {
        'authors': authors,
    }
    return render(request, 'authors.html', context=context)

def author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    # print(author)         atspausdina consolej pycharm

    context = {
        'author': author
    }
    return render(request, 'author.html', context=context)
