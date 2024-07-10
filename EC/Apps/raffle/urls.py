from django.urls import path, include
from . import views

app_name = 'raffle'

urlpatterns = [
    path('raffle_page/', views.raffle, name='raffle_page'),
    path('perform_raffle/', views.perform_raffle, name='perform_raffle'),
    path('manage_prizes/', views.manage_prizes, name='manage_prizes'),
]