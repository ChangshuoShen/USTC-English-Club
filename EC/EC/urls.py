"""EC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index),
    path("admin/", admin.site.urls),
    path('accounts/', include('Apps.accounts.urls', namespace='accounts')),
    path('activities/', include('Apps.activities.urls')),
    path('admin_panel/', include('Apps.admin_panel.urls')),
    path('feedback/', include('Apps.feedback.urls')),
    path('forum/', include('Apps.forum.urls')),
    path('learning/', include('Apps.learning.urls')),
    path('mystery_hunt/', include('Apps.mystery_hunt.urls')),
    path('settings/', include('Apps.settings.urls')),
    path('socialize/', include('Apps.socialize.urls')),
]
