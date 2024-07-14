from django.urls import path

from . import views

urlpatterns = [
    # ex: /secretnote/
    path("", views.createNote, name="note"),
    # ex: /secretnote/5
    path("<str:id>", views.retrieveNote, name="noteview"),
]