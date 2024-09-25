from django.urls import path
from api_v2.views import UserCreateAPIView
urlpatterns = [
    path('register', UserCreateAPIView.as_view(), name='create'),
]