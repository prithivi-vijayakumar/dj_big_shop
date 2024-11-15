from rest_framework.authtoken.models import Token

from django.shortcuts import render,get_object_or_404
from rest_framework import status, generics
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from api_v2.serializers import CustomUserSerializer, CategorySerializer, BrandSerializer, ProductSerializer, \
    SubCategorySerializer, CartSerializer
from backend.models import CustomUser, Category, Brand, Product, SubCategory, Cart
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView

from api_v2.serializers import CustomUserSerializer, EmailAuthTokenSerializer
# Create your views here.
class UserCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({"message": "User successfully registered"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomAuthToken(ObtainAuthToken):
    serializer_class = EmailAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        # return Response({
        #     'token_type':'token',
        #     'token':token.key,
        #     'user_id':user.pk,
        #     'email':user.email
        # })
        return Response(token.key)

class CurrentUserView(APIView):
        permission_classes = [IsAuthenticated]

        def get(self, request):
            user = request.user
            return Response({
                'id': user.id,
                'name': user.email,
                'email': user.email,
                'avatar': user.get_avatar_url(),
            })

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        request.user.auth_token.delete()
        data = {
            'message':'logout was successfully'
        }
        return Response(data=data,status=status.HTTP_200_OK)


class CategoryListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = {
            "data": serializer.data
        }
        return Response(data)


class BrandListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = {
            "data": serializer.data
        }
        return Response(data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = {
            "data": serializer.data
        }
        return Response(data)
class ProductListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = {
            "data": serializer.data
        }
        return Response(data)
class SubCategoryListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class CartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        customer_id = request.user.id
        carts = Cart.objects.filter(custom_user_id=customer_id)
        transformed_carts = CartSerializer(carts, many=True, context={'request': request}).data
        grand_total = Cart.grand_total(customer_id)  # Assuming this is a method in the Cart model
        return Response({'data': transformed_carts, 'grand_total': grand_total}, status=status.HTTP_200_OK)
    def post(self, request):
        customer_id = request.user.id
        product_id = request.data.get('product_id')
        # Ensure product_id is provided in the request
        if not product_id:
            return Response({"error": "Product ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        # Get the product or return 404 if not found
        product = get_object_or_404(Product, id=product_id)
        # Check if the product already exists in the cart
        existing_cart_item = Cart.objects.filter(product_id=product_id, custom_user_id=customer_id).first()
        if existing_cart_item:
            # Update the quantity if the item already exists
            existing_cart_item.qty += 1
            existing_cart_item.save()
            return Response({"message": f"{product.name} quantity updated in your cart."}, status=status.HTTP_200_OK)
        else:
            # Add the item to the cart if it doesn't exist
            Cart.objects.create(product_id=product_id, custom_user_id=customer_id, qty=1)
            return Response({"message": f"{product.name} added to your cart."}, status=status.HTTP_201_CREATED)
class CartItemView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request):
        customer_id = request.user.id
        cart_item_id = request.data.get('cart_id')
        cart_item = Cart.objects.get(id=cart_item_id)
        if not cart_item:
            return Response({"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)
        if cart_item.custom_user_id != customer_id:
            return Response({"error": "You are not authorized to remove this item from the cart."}, status=status.HTTP_403_FORBIDDEN)
        cart_item.delete()
        return Response({"message": "Item removed from your cart."}, status=status.HTTP_200_OK)
    def patch(self, request):
        customer_id = request.user.id
        cart_item_id = request.data.get('cart_id')
        action = request.data.get('action')
        cart_item = Cart.objects.get(id=cart_item_id)
        if not cart_item:
            return Response({"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)
        if cart_item.custom_user_id != customer_id:
            return Response({"error": "You are not authorized to update the quantity of this item in the cart."}, status=status.HTTP_403_FORBIDDEN)
        if action == "increase":
            cart_item.qty += 1
        elif action == "decrease":
            cart_item.qty = max(cart_item.qty - 1, 1)
        else:
            return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)
        cart_item.save()
        return Response({"message": "Quantity updated in your cart."}, status=status.HTTP_200_OK)
class ClearCartView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request):
        customer_id = request.user.id
        Cart.objects.filter(custom_user_id=customer_id).delete()
        return Response({"message": "Cart cleared successfully."}, status=status.HTTP_200_OK)


