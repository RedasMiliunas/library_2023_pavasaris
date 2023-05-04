from django.db import models
import uuid
from django.contrib.auth.models import User
from datetime import date


# Create your models here.
class Genre(models.Model):
    name = models.CharField(verbose_name="Pavadinimas", max_length=50,
                            help_text="Iveskite knygos zanra (pvz.: Detektyvas)")


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Zanras"
        verbose_name_plural = "Zanrai"


class Author(models.Model):
    first_name = models.CharField(verbose_name="Vardas", max_length=50)
    last_name = models.CharField(verbose_name="Pavarde", max_length=50)
    description = models.TextField(verbose_name='Aprasymas', max_length=2000, default="")

    def display_books(self):
        return ', '.join(book.title for book in self.books.all())

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = "Autorius"
        verbose_name_plural = "Autoriai"

class Book(models.Model):
    title = models.CharField(verbose_name="Pavadinimas", max_length=100)
    summary = models.TextField(verbose_name="Aprasymas", max_length=2000)
    isbn = models.CharField(verbose_name="ISBN", max_length=13)
    # author = models.ForeignKey(to="Author", verbose_name="Autorius", on_delete=models.CASCADE)
    # author = models.ForeignKey(to="Author", verbose_name="Autorius", on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(to="Author", verbose_name="Autorius", on_delete=models.SET_NULL, null=True, related_name='books')
    genre = models.ManyToManyField(to="Genre", verbose_name="Zanras")
    cover = models.ImageField(verbose_name='Virselis', upload_to='covers', null=True, blank=True)

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all())

    display_genre.short_description = 'Zanrai'      # panasu i Meta

    def __str__(self):
        return f'{self.title} ({self.author})'

    class Meta:
        verbose_name = "Knyga"
        verbose_name_plural = "Knygos"

class BookInstance(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, help_text="Unikalus ID knygos kopijai")
    book = models.ForeignKey(to="Book", verbose_name="Knyga", on_delete=models.CASCADE, related_name="instances")
    due_back = models.DateField(verbose_name="Bus prieinama", null=True, blank=True)
    reader = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('a', 'Administruojama'),
        ('p', 'Paimta'),
        ('g', 'Galima paimti'),
        ('r', 'Rezervuota')
    )

    status = models.CharField(verbose_name="Busena", max_length=1, choices=LOAN_STATUS, blank=True, default='a')

    def is_overdue(self):
        return self.due_back and date.today() > self.due_back
        # if self.due_back and date.today() > self.due_back:
        #     return True
        # return False

    def __str__(self):
        return f'{self.book.title} {self.uuid} ({self.due_back}) - {self.status}'

    class Meta:
        verbose_name = "Knygos egzempliorius"
        verbose_name_plural = "Knygos egzemplioriai"