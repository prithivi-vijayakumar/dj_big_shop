from django.contrib.auth import login
from django.urls import path
from frontend.views import forget_password, home, register, login_page

urlpatterns = [
    path('', home),
    path('/', home, name='home'),
    path('login', login_page, name='login'),
    path('register', register, name='register'),
    path('forget_password', forget_password),
]