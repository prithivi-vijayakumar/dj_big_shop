from django.urls import path
from frontend.views import forget_password, home

urlpatterns = [
    path('', home),
    path('/', home, name='home'),
    path('forget_password', forget_password),
]