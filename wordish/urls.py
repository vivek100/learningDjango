# wordish/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_page, name='start_page'),
    path('game/', views.game_page, name='game_page'),
]
