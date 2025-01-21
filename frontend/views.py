from django.shortcuts import render, get_object_or_404
from backend.models import Product, Category
# Create your views here.
def home(request):
    return render(request, 'frontend/home.html')
    # Retrieve all categories for use in the view
    categories = Category.objects.all()
    data = {
        'categories': categories,
    }
    return render(request, 'frontend/home.html', data)
def login_page(request):
    return render(request, 'frontend/auth/login.html')
def register(request):
    return render(request, 'frontend/auth/register.html')
def forget_password(request):
    return render(request, 'frontend/auth/forget_password.html')
def account(request):
    return render(request, 'frontend/auth/account.html')
def about(request):
    return render(request, 'frontend/auth/about.html')