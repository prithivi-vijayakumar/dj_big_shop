from django.urls import path
from api_v2.views import UserCreateAPIView
from rest_framework.authtoken.views import obtain_auth_token
from api_v2.views import UserCreateAPIView, CustomAuthToken


urlpatterns = [
    path('register', UserCreateAPIView.as_view(), name='create'),

path('token', obtain_auth_token, name='api_token_auth'),

    path('login', CustomAuthToken.as_view(), name='custom_api_token_auth'),
]
