from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'frontend/home.html')
def forget_password(request):
    return render(request, 'frontend/forget_password.html')