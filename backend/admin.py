from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from backend.forms import CustomerUserCreationForm, CustomerUserChangeForm
from backend.models import CustomUser, NewsLetter, Label, Tag, Discount, Brand, Company, Collection, SubCategory, \
    ProductImage, ProductCategory, ProductLabel, ProductTag, ProductCollection, Cart, Order, OrderItem, Category, \
    Product


# Register your models here.
class CustomUserAdmin(UserAdmin):

    add_form = CustomerUserCreationForm
    form  = CustomerUserChangeForm
    model = CustomUser

    list_display = ('email', 'gender', 'image_tag', 'is_staff', 'is_active',)

    list_filter = ('email', 'is_staff', 'is_active',)

    fieldsets = (
        (None, {'fields': ('email', 'gender', 'password')}),
        ('Permission', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'gender', 'password1','password2', 'is_staff', 'is_active', 'groups', 'user_permissions')}
         ),
    )

    search_fields = ('email',)
    ordering = ('email',)

    def image_tag(self, obj):
        return format_html('<img src ="{}" width ="150" height="150" />'.format(obj.image.url))

    image_tag.short_description = 'Image'

admin.site.register(CustomUser, CustomUserAdmin)

class NewsLetterAdmin(admin.ModelAdmin):

    list_display = ('name', 'email', 'status')

admin.site.register(NewsLetter, NewsLetterAdmin)
class LabelAdmin(admin.ModelAdmin):

    list_display = ('name', 'color', 'status')

admin.site.register(Label, LabelAdmin)

class TagAdmin(admin.ModelAdmin):

    list_display = ('name', 'status')

admin.site.register(Tag, TagAdmin)

class DiscountAdmin(admin.ModelAdmin):

    list_display = ('type', 'start_date', 'end_date', 'never_expired')

admin.site.register(Discount, DiscountAdmin)

class BrandAdmin(admin.ModelAdmin):

    list_display = ('name', 'image_path','image_tag')

    def image_tag(self, obj):
        return  format_html('<img src="{}" width="150" height="150" />'.format(obj.image_path.url))

    image_tag.short_description = 'Image'

admin.site.register(Brand, BrandAdmin)

class CompanyAdmin(admin.ModelAdmin):

    list_display = ('name', 'image_tag', 'user', 'status')

    def image_tag(self, obj):
        return  format_html('<img src="{}" width="150" height="150" />'.format(obj.image_path.url))

    image_tag.short_description = 'Image'

admin.site.register(Company, CompanyAdmin)



# class CategroyAdmin(admin.ModelAdmin):
#
#     list_display = ('name','description', 'selling_price', 'buying_price', 'expected_price', 'earned_price', 'image_tag')
#
#     def image_tag(self, obj):
#         return  format_html('<img src="{}" width="150" height="150" />'.format(obj.image_path.url))
#
#     image_tag.short_description = 'Image'
#
# admin.site.register(Category, CategroyAdmin)

class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Collection, CollectionAdmin)

class SubCategroyAdmin(admin.ModelAdmin):

    list_display = ('name','description', 'selling_price', 'buying_price', 'expected_price', 'earned_price', 'image_tag', 'measurement_unit', 'current_qty', 'reorder_level','company','category')

    def image_tag(self, obj):
        return  format_html('<img src="{}" width="150" height="150" />'.format(obj.image_path.url))

    image_tag.short_description = 'Image'

admin.site.register(SubCategory, SubCategroyAdmin)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of empty forms to display

class ProductCategoryInline(admin.TabularInline):
    model = ProductCategory
    extra = 1

class ProductLabelInline(admin.TabularInline):
    model = ProductLabel
    extra =1

class ProductTagInline(admin.TabularInline):
    model = ProductTag
    extra = 1

class ProductCollectionInline(admin.TabularInline):
    model = ProductCollection
    extra = 1

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'custom_user', 'product', 'qty', )
    def image_tag(self, obj):
        return format_html('<img src = "{}" width="150" height="150" />'.format(obj.product.image.url))
admin.site.register(Cart, CartAdmin)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Number of empty forms to display
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order_date', 'total_amount', 'order_status', 'payment_method', 'order_number')
    list_filter = ('order_status', 'payment_method', 'order_date')
    search_fields = ('order_number', 'customer__username')  # Assuming CustomUser has a username field
    readonly_fields = ('order_number', 'order_date')  # Fields that should be read-only
    inlines = [OrderItemInline]  # Display OrderItem as inline within Order admin
    def get_readonly_fields(self, request, obj=None):
        # Additional logic to determine read-only fields
        if obj:  # If editing an existing object
            return self.readonly_fields + ('total_amount',)
        return self.readonly_fields
admin.site.register(Order, OrderAdmin)




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'selling_price', 'buying_price', 'status')
    search_fields = ('name',)
    list_filter = ('status',)
    inlines = [ProductCategoryInline]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)
    search_fields = ('name',)
    list_filter = ('category',)
    inlines = [ProductCategoryInline, ProductTagInline, ProductLabelInline, ProductCollectionInline, ProductImageInline]
admin.site.register(ProductCategory)