from django.shortcuts import render, get_object_or_404, redirect, reverse
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

from django.views.generic.edit import FormMixin
from .forms import BookReviewForm

class BookDetailView(FormMixin, generic.DetailView):
    model = Book
    context_object_name = "book"
    template_name = "book.html"
    form_class = BookReviewForm

    def get_success_url(self):
        return reverse('book', kwargs={'pk': self.object.id})

    #Jo tiesiog reikia:
        # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

# dabar jau paspaudus submit po komentaro nukelia atgal i ta pati book.html
# štai čia nurodome, kad knyga bus būtent ta, po kuria komentuojame, o vartotojas bus tas, kuris yra prisijungęs.
    def form_valid(self, form):
        form.instance.book = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super().form_valid(form)


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


class BookInstanceListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    context_object_name = 'instances'
    template_name = 'instances.html'


class BookInstanceDetailView(LoginRequiredMixin, generic.DetailView):
    model = BookInstance
    context_object_name = 'instance'
    template_name = 'instance.html'


class BookInstanceCreatView(LoginRequiredMixin, generic.CreateView):
    model = BookInstance
    fields = ['book', 'due_back']
    success_url = '/instances'
    template_name = 'instance_form.html'

    def form_valid(self, form):
        form.instance.reader = self.request.user
        return super().form_valid(form)

from django.contrib.auth.mixins import UserPassesTestMixin
class BookInstanceUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = BookInstance
    fields = ['book', 'due_back']
    success_url = '/instances'
    template_name = 'instance_form.html'

    def form_valid(self, form):
        form.instance.reader = self.request.user
        return super().form_valid(form)

    def test_func(self):
        instance = self.get_object()
        return instance.reader == self.request.user

from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.models import User

@csrf_protect
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} uzimtas!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. pastu {email} jau uzregistruotas!')
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} uzregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, f'Slaptazodziai nesutampa')
            return redirect('register')
    else:
        return render(request, 'registration/register.html')

from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.info(request, f'Profilis sekmingai atnaujintas!')
            return redirect('profile')
        else:
            messages.error(request, f'Kazka blogai vedi...')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'profile.html', context=context)

#pirmas bandymas:
# def profile(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         if User.objects.filter(username=username).exists():
#             messages.error(request, f'Vartotojo vardas {username} uzimtas!')
#             return redirect('profile')
#         else:
#             if User.objects.filter(email=email).exists():
#                 messages.error(request, f'Vartotojas su el. pastu {email} jau uzregistruotas!')
#                 return redirect('profile')
#             if request.method == 'POST':
#
#                 u_form = UserUpdateForm(request.POST, instance=request.user)
#                 p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
#                 if u_form.is_valid() and p_form.is_valid():
#                     u_form.save()
#                     p_form.save()
#                     messages.info(request, f'Profilis sekmingai atnaujintas!')
#                     return redirect('profile')
#
#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         p_form = ProfileUpdateForm(instance=request.user.profile)
#
#     context = {
#         'u_form': u_form,
#         'p_form': p_form,
#     }
#
#     return render(request, 'profile.html', context=context)

#antras bandymas:
# def profile(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
#             messages.error(request, f'Vartotojo vardas {username} arba el. pastas {email} yra uzimtas!')
#             return redirect('profile')
#         else:
#             u_form = UserUpdateForm(request.POST, instance=request.user)
#             p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
#             if u_form.is_valid() and p_form.is_valid():
#                 u_form.save()
#                 p_form.save()
#                 messages.info(request, f'Profilis sekmingai atnaujintas!')
#                 return redirect('profile')
#
#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         p_form = ProfileUpdateForm(instance=request.user.profile)
#
#     context = {
#         'u_form': u_form,
#         'p_form': p_form,
#     }
#
#     return render(request, 'profile.html', context=context)

#trecias bandymas:
# def profile(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         if User.objects.filter(username=username).exists():
#             messages.error(request, f'Vartotojo vardas {username} uzimtas!')
#             return redirect('profile')
#         elif User.objects.filter(email=email).exists():
#                 messages.error(request, f'Vartotojas su el. pastu {email} jau uzregistruotas!')
#                 return redirect('profile')
#         else:
#              u_form = UserUpdateForm(request.POST, instance=request.user)
#              p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
#              if u_form.is_valid() and p_form.is_valid():
#                  u_form.save()
#                  p_form.save()
#                  messages.info(request, f'Profilis sekmingai atnaujintas!')
#                  return redirect('profile')
#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         p_form = ProfileUpdateForm(instance=request.user.profile)
#
#     context = {
#         'u_form': u_form,
#         'p_form': p_form,
#     }
#
#     return render(request, 'profile.html', context=context)