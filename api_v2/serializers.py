from rest_framework import serializers
from backend.models import CustomUser, Category, Brand, Label, ProductLabel, ProductCategory, Tag, ProductTag, \
    Collection, ProductCollection, ProductImage, Product, SubCategory, Cart, Order, OrderItem
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = [
            'gender',
            'password',
            'email'
        ]
    def create(self, validated_data):
        user = super(CustomUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        # group = Group.objects.get(name='EMPLOYEE')
        # user.groups.add(group)
        user.is_staff = True
        user.is_active = True
        user.save()
        return user

class EmailAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_("Email"))
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'), username=email, password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image_path']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'image_path']


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name']
class ProductLabelSerializer(serializers.ModelSerializer):
    label = LabelSerializer()
    class Meta:
        model = ProductLabel
        fields = ['label', 'added_on']
class ProductCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = ProductCategory
        fields = ['category', 'added_on']
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
class ProductTagSerializer(serializers.ModelSerializer):
    tag = TagSerializer()
    class Meta:
        model = ProductTag
        fields = ['tag', 'added_on']
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'name']
class ProductCollectionSerializer(serializers.ModelSerializer):
    collection = CollectionSerializer()
    class Meta:
        model = ProductCollection
        fields = ['collection', 'added_on']
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']
class ProductSerializer(serializers.ModelSerializer):
    productLabel = ProductLabelSerializer(source='productlabel_set', many=True)
    categories = ProductCategorySerializer(source='productcategory_set', many=True)
    productTag = ProductTagSerializer(source='producttag_set', many=True)
    productCollection = ProductCollectionSerializer(source='productcollection_set', many=True)
    brand = BrandSerializer()
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'qty',
            'alert_stock',
            'brand',
            'categories',
            'productTag',
            'productLabel',
            'productCollection',
            'images'
        ]

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name']

class CartSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    product_id = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    product_image = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = '__all__'
    def get_customer_name(self, obj):
        return obj.custom_user.email if obj.custom_user else None
    def get_product_id(self, obj):
        return obj.product.id if obj.product else None
    def get_product_name(self, obj):
        return obj.product.name if obj.product else None
    def get_product_image(self, obj):
        if obj.product and obj.product.images.exists():
            request = self.context.get('request')
            image_url = obj.product.images.first().image.url
            return request.build_absolute_uri(image_url) if request else image_url
        return None
    # 'product_image']
    # def get_product_image(self, obj):
    #     request = self.context.get('request')
    #     if request is not None:
    #         return request.build_absolute_uri(obj.product.image.url)
    #     return obj.product.image.url
    def get_price(self, obj):
        return obj.product.price if obj.product else None

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'qty', 'unit_price', 'amount', 'discount']
class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'total_amount', 'order_status', 'payment_method', 'order_items']
        read_only_fields = ['customer']  # Ensure customer is not required in the request
    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        # order = Order.objects.create(**validated_data)
        user = self.context['request'].user
        order = Order.objects.create(customer=user, **validated_data)
        total_amount = 0
        for item_data in order_items_data:
            # Calculate the amount here
            amount = item_data['qty'] * item_data['unit_price']
            total_amount += amount
            # Create OrderItem without passing amount directly
            OrderItem.objects.create(
                order=order,
                product=item_data['product'],
                qty=item_data['qty'],
                unit_price=item_data['unit_price'],
                amount=item_data['amount'],
                discount=item_data['discount']
            )
        # Update total_amount for the order
        order.total_amount = total_amount
        order.save()
        return order