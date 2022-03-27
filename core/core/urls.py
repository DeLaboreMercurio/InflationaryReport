"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path

from core.views.home import home_view
from core.views.users import register_request, login_request, logout_request

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_view, name="home"),
    path("users/registration/", register_request, name="register"),
    path("users/login/", login_request, name="login"),
    path("users/logout/", logout_request, name="logout"),
]
