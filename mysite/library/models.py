from django.db import models
import uuid


# Create your models here.
class Genre(models.Model):
    name = models.CharField(verbose_name="Pavadinimas", max_length=50,
                            help_text="Iveskite knygos zanra (pvz.: Detektyvas)")

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(verbose_name="Vardas", max_length=50)
    last_name = models.CharField(verbose_name="Pavarde", max_length=50)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Book(models.Model):
    title = models.CharField(verbose_name="Pavadinimas", max_length=100)
    summary = models.TextField(verbose_name="Aprasymas", max_length=2000)
    isbn = models.CharField(verbose_name="ISBN", max_length=13)
    # author = models.ForeignKey(to="Author", verbose_name="Autorius", on_delete=models.CASCADE)
    author = models.ForeignKey(to="Author", verbose_name="Autorius", on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField(to="Genre", verbose_name="Zanras")


    def __str__(self):
        return f'{self.title} ({self.author})'

class BookInstance(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, help_text="Unikalus ID knygos kopijai")
    book = models.ForeignKey(to="Book", verbose_name="Knyga", on_delete=models.CASCADE)
    due_back = models.DateField(verbose_name="Bus prieinama", null=True, blank=True)

    LOAN_STATUS = (
        ('a', 'Administruojama'),
        ('p', 'Paimta'),
        ('g', 'Galima paimti'),
        ('r', 'Rezervuota')
    )

    status = models.CharField(verbose_name="Busena", max_length=1, choices=LOAN_STATUS, blank=True, default='a')

    def __str__(self):
        return f'{self.book.title} {self.uuid} ({self.due_back}) - {self.status}'