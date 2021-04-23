from django.urls import path

from .views import Gateway, Signup, Login, Profile

urlpatterns = [
    path('main', Gateway.as_view({'post': 'handle_request'})),
    path('signup', Signup.as_view({'post': 'handle_request'})),
    path('login', Login.as_view({'post': 'handle_request'})),
    path('profile', Profile.as_view({'post': 'handle_request'})),
]