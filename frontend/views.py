from django.shortcuts import render

# Create your views here.
def forget_password(request):
    return render(request, 'frontend/forget_password.html')