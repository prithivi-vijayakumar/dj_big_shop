from django.shortcuts import render, get_object_or_404
from backend.models import Product, Category
# Create your views here.
def home(request):
    return render(request, 'frontend/home.html')
    # Retrieve all categories for use in the view
    categories = Category.objects.all()
    category_present = 'category' in request.GET
    data = {
        'categories': categories,
        'category_present': category_present,
    }
    category_id = request.GET.get('category')
    if category_id and category_id != 'All':
        # Filter products based on the selected category
        products = Product.objects.filter(category__id=category_id)
        
        # Get the category object and set page title and product count
        category = get_object_or_404(Category, pk=category_id)
        data['page_title'] = category.name
        data['product_count'] = category.products.count()

        # Pass filtered products to the template
        data['products'] = products
        return render(request, 'frontend/product/list/type1.html', data)

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