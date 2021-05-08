from django.urls import path

from . import views

urlpatterns = [
    path("<str:username>", views.stats, name="stats")
]
