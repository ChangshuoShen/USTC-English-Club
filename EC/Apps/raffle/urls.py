from django.urls import path, include
from . import views

app_name = 'forum'

urlpatterns = [
    path('draw', views.draw, name='draw'),
]