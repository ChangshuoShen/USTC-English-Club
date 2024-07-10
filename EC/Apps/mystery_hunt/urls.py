from django.urls import path
# import Apps.accounts.views as views
from . import views
app_name = 'mystery_hunt'

urlpatterns = [
    # path('login/', views.login),
    path('hunt_index', views.hunt_index, name='hunt_index'),
    path('hunt_detail<int:riddle_id>', views.hunt_detail, name='hunt_detail'),
]

