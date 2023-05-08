from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("authors/", views.authors, name="authors"),
    path("authors/<int:author_id>", views.author, name="author"),
    path("books/", views.BookListView.as_view(), name="books"),
    path("books/<int:pk>", views.BookDetailView.as_view(), name="book"), #klasei nereikia book_id
    path("search/", views.search, name="search"),
    path('my_books/', views.MyBookInstanceListView.as_view(), name='my_books'),
    path('register/', views.register, name='register'),
]