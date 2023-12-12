from django.urls import path
from .views import ImageFinder

urlpatterns = [
    path('search/', ImageFinder.as_view()),
]
