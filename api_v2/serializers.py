from rest_framework import serializers
from backend.models import CustomUser, Category, Brand, Label, ProductLabel, ProductCategory, Tag, ProductTag, \
    Collection, ProductCollection, ProductImage, Product
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