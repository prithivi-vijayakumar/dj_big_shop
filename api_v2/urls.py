from django.urls import path
from api_v2.views import UserCreateAPIView, LogoutAPIView, CategoryListView,CurrentUserView,BrandListView,ProductListView,SubCategoryListView
from rest_framework.authtoken.views import obtain_auth_token
from api_v2.views import UserCreateAPIView, CustomAuthToken




urlpatterns = [
    path('register', UserCreateAPIView.as_view(), name='create'),

path('token', obtain_auth_token, name='api_token_auth'),

    path('login', CustomAuthToken.as_view(), name='custom_api_token_auth'),
    path('user', CurrentUserView.as_view(), name='current-user'),
    path('user', CurrentUserView.as_view(), name='current-user'),
    path('logout', LogoutAPIView.as_view(), name='logout'),
    path('categories', CategoryListView(), name = 'category_list'),
    path('brands', BrandListView.as_view(), name = 'brand_list'),
    path('products', ProductListView.as_view(), name='product_list'),
    path('subcategories', SubCategoryListView.as_view(), name='subcategory_list'),
]
