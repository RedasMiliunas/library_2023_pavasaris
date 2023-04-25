from django.contrib import admin
from . import models

# reikia sukurti admin klase, kurioje nustatysime
# kaip norime pagal savo poreikius, kaip bus atvaizduotas koks nors rodinys

class BooksInstanceInline(admin.TabularInline):
    model = models.BookInstance
    extra = 0   #isjungia papildomas tuscias eilutes, kad nepridetu tusciu irasu papildomai
    readonly_fields = ['uuid']      #jeigu norim, kad kazkuris laukas nebutu galimas redaguoti
    # can_delete = False          # jeigu norim padaryti, kad per ta psl neitu istrinti irasu

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'isbn', 'author', 'display_genre']
    #pridedam eilute cia del inline dalyko:
    inlines = [BooksInstanceInline]

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'book', 'status', 'due_back']
    list_filter = ['status', 'due_back', 'book']
    #nustatom filtra
    fieldsets = (
        ('General', {'fields': ('uuid', 'book')}),
        ('Availability', {'fields': ('status', 'due_back')}),
    )



# Register your models here.
admin.site.register(models.Author)
admin.site.register(models.Genre)
# admin.site.register(models.Book)
admin.site.register(models.Book, BookAdmin)     # cia turim uzregistruoti su klases pavadinimu per kableli!
# admin.site.register(models.BookInstance)
admin.site.register(models.BookInstance, BookInstanceAdmin)

