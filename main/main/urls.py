"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path

from account.views import Gateway, Signup, Login, Profile

urlpatterns = [
    path('main', Gateway.as_view({'post': 'handle_request'})),
    path('signup', Signup.as_view({'post': 'handle_request'})),
    path('login', Login.as_view({'post': 'handle_request'})),
    path('profile', Profile.as_view({'post': 'handle_request'})),
]
