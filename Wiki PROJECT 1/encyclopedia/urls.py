from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name='entry'),
    path("search/", views.search, name="search"),
    path("create/", views.create, name="create"),
    path("edit/", views.edit, name="edit"),
    path("save/", views.save, name="save"),
    path("choice/", views.choice, name="choice"),
    path("delete/<str:title>", views.delete, name="delete"),
]

   
