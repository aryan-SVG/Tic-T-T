from django.urls import path
from . import views

urlpatterns = [
    path('', views.x, name='x'),
    path('', views.o, name='o'),
    path('', views.game, name='game'),
]
