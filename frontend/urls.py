from django.urls import path
from frontend.views import forget_password
urlpatterns = [
    path('forget_password', forget_password),
]