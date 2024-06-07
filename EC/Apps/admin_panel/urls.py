from django.urls import path
from . import views

app_name = "admin_panel"

urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"),
    path('post_list', views.post_list, name="post_list"),
    path('riddles/', views.riddles, name="riddles"),
    path('share_sth_interesting/', views.share_sth_interesting, name="share_sth_interesting"),
    path('ask_for_help/', views.ask_for_help, name="ask_for_help"),
    path('find_friends', views.find_friends, name="find_friends"),
    path("else/", views.else_list, name="else"),
]

