from django.urls import path
from api_v2.views import UserCreateAPIView, LogoutAPIView
from rest_framework.authtoken.views import obtain_auth_token
from api_v2.views import UserCreateAPIView, CustomAuthToken


class CurrentUserView:
    pass


class CategoryListView:
    pass


urlpatterns = [
    path('register', UserCreateAPIView.as_view(), name='create'),

path('token', obtain_auth_token, name='api_token_auth'),

    path('login', CustomAuthToken.as_view(), name='custom_api_token_auth'),
    path('user', CurrentUserView.as_view(), name='current-user'),
    path('user', CurrentUserView.as_view(), name='current-user'),
    path('logout', LogoutAPIView.as_view(), name='logout'),
    path('categories', CategoryListView.as_view(), name = 'category_list'),
]
