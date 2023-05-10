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
    path('profile/', views.profile, name='profile'),
    path('instances/', views.BookInstanceListView.as_view(), name='instances'),
    path('instances/<int:pk>', views.BookInstanceDetailView.as_view(), name='instance'),
    path('instances/new', views.BookInstanceCreatView.as_view(), name='instance_new'),
    path('instances/<int:pk>/update', views.BookInstanceUpdateView.as_view(), name='instance_update'),
    path('instances/<int:pk>/delete', views.BookInstanceDeleteView.as_view(), name='instance_delete'),
]


