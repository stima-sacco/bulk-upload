from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from app.models import Car, CarBrand, ExtraCarImage

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

class CarAdmin(admin.ModelAdmin):
    list_display = ("id", "brand", "make", "vendor", "engine_size","location","price","posting_paid","posting_transaction_id","date_added")
    list_filter = ("id", "make", "vendor", "engine_size","location","price","posting_paid","posting_transaction_id","date_added")
    search_fields = ["id", "make", "vendor", "engine_size","location","price","posting_paid","posting_transaction_id","date_added"]

    ordering = ('-id','brand','make')

class CarBrandAdmin(admin.ModelAdmin):
    list_display = ("id", "name","car_brand_date_added")
    list_filter = ("id", "name","car_brand_date_added")
    search_fields = ["id", "name","car_brand_date_added"]

    ordering = ('name',)

class ExtraCarImageAdmin(admin.ModelAdmin):
    list_display = ("id", "car_id","car","car_image")
    list_filter = ("id", "car_id","car","car_image")
    search_fields = ["id", "car_id","car","car_image"]

    ordering = ('id','car')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(CarBrand, CarBrandAdmin)
admin.site.register(ExtraCarImage, ExtraCarImageAdmin)
admin.site.site_header = 'Bulk_upload'
admin.site.site_title = 'Bulk_upload'
admin.site.index_title = 'Feature Areas'
