from django.contrib import admin
from . import models

# reikia sukurti admin klase, kurioje nustatysime
# kaip norime pagal savo poreikius, kaip bus atvaizduotas koks nors rodinys

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'isbn', 'author', 'display_genre']

# Register your models here.
admin.site.register(models.Author)
admin.site.register(models.Genre)
# admin.site.register(models.Book)
admin.site.register(models.Book, BookAdmin)     # cia turim uzregistruoti su klases pavadinimu per kableli!
admin.site.register(models.BookInstance)

