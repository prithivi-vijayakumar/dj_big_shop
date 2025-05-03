from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from api_v2.views import UserCreateAPIView, CustomAuthToken, CurrentUserView, LogoutAPIView, CategoryListView, \
    BrandListView, ProductListView, SubCategoryListView, CartView, CartItemView, ClearCartView, OrderListView, \
    OrderDetailView

urlpatterns = [
    path('register', UserCreateAPIView.as_view(), name='create'),

    # Login Type 1
    path('token', obtain_auth_token, name='api_token_auth'),

    # Login Type 2
    path('login', CustomAuthToken.as_view(), name='custom_api_token_auth'),

    path('user', CurrentUserView.as_view(), name='current-user'),

    # Logout
    path('logout', LogoutAPIView.as_view(), name='logout'),

    # Category
    path('categories', CategoryListView.as_view(), name = 'category_list'),

    # Brand
    path('brands', BrandListView.as_view(), name = 'brand_list'),

    # Product
    path('products', ProductListView.as_view(), name='product_list'),

    # Sub Category
    path('subcategories', SubCategoryListView.as_view(), name='subcategory_list'),

    # Cart
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/item/', CartItemView.as_view(), name='cart-item'),
    path('clear-cart', ClearCartView.as_view(), name='clear-cart'),

    # Order
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),


]