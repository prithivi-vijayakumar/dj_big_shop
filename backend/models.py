from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

# Create your models here.
from backend.manager import CustomerUserManager
import datetime


class Gender(models.TextChoices):
    MALE = 'M', _('Male')
    FEMALE = 'F', _('Female')


class GenderedImageField(models.ImageField):
    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        if not value or not hasattr(model_instance, self.attname):

            gender = model_instance.gender if hasattr(model_instance, 'gender') else Gender.MALE

            if gender == Gender.MALE:
                value = 'profile/male_avatar.png'
            elif gender == Gender.FEMALE:
                value = 'profile/female_avatar.png'
            else:
                value = 'profile/default_image.jpg'

        elif model_instance.gender != getattr(model_instance, f"{self.attname}_gender_cache", None):
            gender = model_instance.gender
            if gender == Gender.MALE:
                value = 'profile/male_avatar.png'
            elif gender == Gender.FEMALE:
                value = 'profile/female_avatar.png'
            else:
                value = 'profile/default_image.jpg'
        setattr(model_instance, f"{self.attname}_gender_cache", model_instance.gender)
        return value


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.MALE)
    image = GenderedImageField(upload_to='profile/', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['gender']
    objects = CustomerUserManager()

    def __str__(self):
        return self.email

class NewsLetterStatus(models.TextChoices):
    SUBSCRIBE = 'SUBSCRIBE', _('SUBSCRIBE')
    UNSUBSCRIBE = 'UNSUBSCRIBE', _('UNSUBSCRIBE')

class NewsLetter(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email =models.EmailField(_('email address'), unique=True)
    status= models.CharField(
        max_length=255,
        choices=NewsLetterStatus.choices,
        default=NewsLetterStatus.SUBSCRIBE
    )
    def __str__(self):
        return self.email

    class Meta:
        db_table = 'news_letter'


class LabelStatus(models.TextChoices):
    PROCESSING = 'PROCESSING', _('PROCESSING')
    ACTIVE = 'ACTIVE', _('ACTIVE')
    HIDE = 'HIDE', _('HIDE')

class Label(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    color = models.CharField(max_length=255,null=True, blank=True)
    status= models.CharField(
        max_length=255,
        choices=LabelStatus.choices,
        default=LabelStatus.PROCESSING
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'label'

class TagStatus(models.TextChoices):
    PUBLISHED = 'PUBLISHED', _('PUBLISHED')
    DRAFT = 'DRAFT', _('DRAFT')
    PENDING = 'PENDING', _('PENDING')

class Tag(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    status=models.CharField(
        max_length=255,
        choices=TagStatus.choices,
        default=TagStatus.PUBLISHED
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tag'

class DiscountStatus(models.TextChoices):
    COUPON_CODE = 'COUPON_CODE', _('COUPON_CODE')
    PROMOTION = 'PROMOTION', _('PROMOTION')

class Discount(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    start_date= models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    never_expired= models.BooleanField(default=False)
    status = models.CharField(
        max_length=255,
        choices=DiscountStatus.choices,
        default=DiscountStatus.COUPON_CODE
    )

    def __str__(self):
        return str(self.type)

    class Meta:
        db_table = 'discount'


class BrandStatus(models.TextChoices):
    PUBLISHED = 'PUBLISHED', _('PUBLISHED')
    DRAFT = 'DRAFT', _('DRAFT')
    PENDING = 'PENDING', _('PENDING')

class Brand(models.Model):
    id = models.BigAutoField(primary_key=True)
    name= models.CharField(max_length=255)
    image_path= models.ImageField(upload_to='brands', null=True, blank=True, default='No_image_available.jpg')
    status= models.CharField(
        max_length=255,
        choices=BrandStatus.choices,
        default=BrandStatus.PUBLISHED
    )

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'brand'

class CompanyStatus(models.TextChoices):
    PUBLISHED = 'PUBLISHED', _('PUBLISHED')
    DRAFT = 'DRAFT', _('DRAFT')
    PENDING = 'PENDING', _('PENDING')

class Company(models.Model):
    id = models.BigAutoField(primary_key=True)
    name= models.CharField(max_length=255)
    image_path = models.ImageField(upload_to='company', null=True, blank=True,default='No_image_available.jpg')
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(
        max_length=255,
        choices=CompanyStatus.choices,
        default=CompanyStatus.PUBLISHED
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'company'


class CategoryStatus(models.TextChoices):
    PUBLISHED = 'PUBLISHED', _('PUBLISHED')
    DRAFT = 'DRAFT', _('DRAFT')
    PENDING = 'PENDING', _('PENDING')

class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name= models.CharField(max_length=255)
    description = models.TextField(null=True,blank=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    expected_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    earned_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image_path= models.ImageField(upload_to='brands', null=True, blank=True, default='No_image_available.jpg')
    status= models.CharField(
        max_length=255,
        choices=CategoryStatus.choices,
        default=CategoryStatus.PUBLISHED
    )

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'category'

class CollectionStatus(models.TextChoices):
    PUBLISHED = 'PUBLISHED', _('PUBLISHED')
    DRAFT = 'DRAFT', _('DRAFT')
    PENDING = 'PENDING', _('PENDING')

class Collection(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=255,
        choices=CollectionStatus.choices,
        default=CollectionStatus.PUBLISHED
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'collection'

        class SubCategoryStatus(models.TextChoices):
            PUBLISHED = 'PUBLISHED', _('PUBLISHED')
            DRAFT = 'DRAFT', _('DRAFT')
            PENDING = 'PENDING', _('PENDING')

class SubCategoryStatus(models.TextChoices):
    PUBLISHED = 'PUBLISHED', _('PUBLISHED')
    DRAFT = 'DRAFT', _('DRAFT')
    PENDING = 'PENDING', _('PENDING')

class SubCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name= models.CharField(max_length=255)
    description = models.TextField(null=True,blank=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    expected_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    earned_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image_path= models.ImageField(upload_to='brands', null=True, blank=True, default='No_image_available.jpg')
    measurement_unit= models.CharField(max_length=255, null=True, blank=True)
    current_qty= models.IntegerField(null=True, blank=True)
    reorder_level= models.IntegerField(null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True ,blank=True)
    status= models.CharField(
        max_length=255,
        choices=SubCategoryStatus.choices,
        default=SubCategoryStatus.PUBLISHED
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sub_category'


class StockStatus(models.TextChoices):
    IN_STOCK = 'IN_STOCK', _('IN_STOCK')
    OUT_OF_STOCK = 'OUT_OF_STOCK', _('OUT_OF_STOCK')
    ON_BACK_ORDER = 'ON_BACK_ORDER', _('ON_BACK_ORDER')

class ProductStatus(models.TextChoices):
    PUBLISHED = 'PUBLISHED', _('PUBLISHED')
    DRAFT = 'DRAFT', _('DRAFT')
    PENDING = 'PENDING', _('PENDING')

class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    qty= models.IntegerField(null=True, blank=True)
    alert_stock =  models.IntegerField(null=True,blank=True)
    is_featured = models.BooleanField(default=False)
    min_order_qty = models.IntegerField(null=True, blank=True)
    max_order_qty = models.IntegerField(null=True, blank=True)
    categories = models.ManyToManyField('Category', related_name='products', through='ProductCategory')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    productTag = models.ManyToManyField('Tag', related_name='tags', through='ProductTag')
    productLabel = models.ManyToManyField('Label', related_name='labels', through='ProductLabel')
    productCollection = models.ManyToManyField('Collection', related_name='collections', through='ProductCollection')
    stock_status = models.CharField(
        max_length=255,
        choices=StockStatus.choices,
        default=StockStatus.IN_STOCK
    )
    status = models.CharField(
        max_length=255,
        choices=ProductStatus.choices,
        default=ProductStatus.PUBLISHED
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', default='No_image_available.jpg')

    def __str__(self):
        return f"Image for {self.product.name}"


@receiver(post_save, sender=Product)
def create_default_product_image(sender, instance, created, **kwargs):
    if created:
        # Check if the product already has images
        if not instance.images.exists():
            # Create a default image
            ProductImage.objects.create(
                product=instance
                # image='product_images/No_image_available.jpg'
            )

class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'product_category'
        unique_together = (('product', 'category'),)

class ProductLabel(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'product_label'
        unique_together = (('product', 'label'),)

class ProductTag(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'product_tag'
        unique_together = (('product', 'tag'),)

class ProductCollection(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'product_collection'
        unique_together = (('product', 'collection'),)

class Cart(models.Model):
    id = models.BigAutoField(primary_key=True)
    custom_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    qty = models.IntegerField()
    product_image = models.ImageField(upload_to='carts', null=True, blank=True, default='No_image_available.jpg')
    def __str__(self):
        return str(self.qty)
    def total_price(self):
        return self.qty * self.product.price if self.product else 0
    # def grand_total(self):
    #     cart_items = Cart.objects.filter(custom_user=self.custom_user)
    #     total = sum(element.total_price() for element in cart_items)
    #     return total
    @classmethod
    def grand_total(cls, customer_id):
        cart_items = cls.objects.filter(custom_user_id=customer_id)
        total = sum(item.total_price() for item in cart_items)
        return total
    class Meta:
        db_table = 'cart'


class OrderStatus(models.TextChoices):
    PENDING = 'PENDING', _('Pending')
    CONFIRMED = 'CONFIRMED', _('Confirmed')
    DELIVERY = 'DELIVERY', _('Delivery')
class PaymentMethodStatus(models.TextChoices):
    CASH = 'CASH', _('CASH')
    UPI = 'UPI', _('UPI')
    CARD = 'CARD', _('ON_BACK_ORDER')
class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20, unique=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    order_status = models.CharField(
        max_length=255,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )
    payment_method = models.CharField(
        max_length=255,
        choices=PaymentMethodStatus.choices,
        default=PaymentMethodStatus.CASH
    )
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)
    def generate_order_number(self):
        today = datetime.date.today().strftime('%Y-%m-%d')
        last_order = Order.objects.filter(order_date__date=today).order_by('-id').first()
        if last_order:
            last_number = int(last_order.order_number.split()[-1])
            next_number = str(last_number + 1).zfill(3)
        else:
            next_number = '001'
        return f"{today} {next_number}"
    def __str__(self):
        return f"{self.order_date.strftime('%d-%m-%Y %H:%M:%S')} {self.customer} {self.total_amount}"
    class Meta:
        db_table = 'order'


class OrderItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    # order = models.ForeignKey(Order, on_delete=models.CASCADE)
    # order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    qty = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField()
    # item_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    def __str__(self):
        return f"{self.order} {self.product.name} {self.qty} {self.unit_price} {self.amount}"
    class Meta:
        db_table = 'orderitem'