from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Book, BookInstance, Author
from django.views import generic

#kad per funkcija padaryti puslapiavima:
from django.core.paginator import Paginator
#pridedant paieska (search lauka)
from django.db.models import Q

# Create your views here.

# cia backendo darbas

def index(request):
    # return HttpResponse("Labas, pasauli!")
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_authors = Author.objects.count()

    # filtruojam available knygas
    num_instances_available = BookInstance.objects.filter(status__exact='g').count()

    num_visits = request.session.get("num_visits", 1)
    request.session['num_visits'] = num_visits + 1

    #sudedam visus i masyva:
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_authors': num_authors,
        'num_instances_available': num_instances_available,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)

# dabar frontend'as.

# django V - views.
# Views: gali buti function-base (kaip virsuje) arba
# class-base (daugiau django pasirinkimas - supaprastina darba): kuriam funkcija arba klase views.py faile!!
# galim juos miksuoti, taikyti pagal tai kas patogiau kuriam veiksmui atlikti.
# class-base: jeigu lendam giliau, reikia kazka keisti, tuomet reikes daryti komplikuociau - daryti overwrite'us klases metodams ir pan.

def authors(request):
    paginator = Paginator(Author.objects.all(), 3)
    page_number = request.GET.get('page')
    paged_authors = paginator.get_page(page_number)
    authors = paged_authors
    # authors = Author.objects.all()
    context = {
        'authors': authors,
    }
    return render(request, 'authors.html', context=context)

def author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)        # pk = primarykey
    # print(author)         atspausdina consolej pycharm - pasitikrinimui ar veikia

    context = {
        'author': author
    }
    return render(request, 'author.html', context=context)

#search view'as:
def search(request):
    query = request.GET.get('query')
    search_results = Book.objects.filter(Q(title__icontains=query) | Q(summary__icontains=query) | Q(author__first_name__icontains=query) | Q(author__last_name__icontains=query))
    context = {
        'books': search_results,
        'query': query,
    }
    return render(request, 'search.html', context=context)

# class-base view:
class BookListView(generic.ListView):
    model = Book
    context_object_name = "books"       #sitas nera butinas - sugeneruos auto pavadinima
    template_name = "books.html"        # irgi generuoja auto, bet del aiskumo isivedam taip - geriau!
    paginate_by = 3                     # puslapiuojam!

# papildomas parametras 'queryset' - pasiziureti mokymo medziagoje! (CBV - class-based view)

class BookDetailView(generic.DetailView):
    model = Book
    context_object_name = "book"
    template_name = "book.html"


from django.contrib.auth.mixins import LoginRequiredMixin


class MyBookInstanceListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    context_object_name = 'my_books'
    template_name = 'my_books.html'

    # paginate_by = 10
    #filtruojam tik tas knygas, kuriu mums reikia (kuriu useris = self.request.user)
    def get_queryset(self):
        return BookInstance.objects.filter(reader=self.request.user)
            # .filter(status__exact='p').order_by('due_back')