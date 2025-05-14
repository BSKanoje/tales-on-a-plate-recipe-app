# recipe/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('my-recipes/', views.my_recipes, name='my_recipes'),
]