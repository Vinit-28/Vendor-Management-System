from django.urls import path
from users.views import UserRegistration, LoginView

urlpatterns = [
    path('users/registration/', UserRegistration.as_view(), name='user_registarion'),
    path('users/login/', LoginView.as_view(), name='user_login')
]