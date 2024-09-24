from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from backend.forms import CustomerUserCreationForm, CustomerUserChangeForm
from backend.models import CustomUser, NewsLetter, Label, Tag, Discount, Brand, Company, Collection, SubCategory, \
    ProductImage, ProductCategory, ProductLabel, ProductTag


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