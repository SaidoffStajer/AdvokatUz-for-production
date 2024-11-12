
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from accounts import models


class RegionInline(admin.StackedInline):
    model = models.Region
    extra = 0
    fields = ['name',]


class CityInline(admin.StackedInline):
    model = models.City
    extra = 0
    fields = ['link', 'name']
    readonly_fields = ['link',]

    def link(self, instance):
        url = f'http://localhost:8000/admin/accounts/city/{instance.id}/change/'
        return mark_safe(f'<a href="{url}">Kirish</a>')


@admin.register(models.User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (_("User choices"), {"fields": ("auth_type", "user_role", 'gender')}),
        (_("Location"), {"fields": ("location_text", "latitude", 'longitude')}),
        (_("Permissions"),{"fields": ("is_active","is_staff","is_superuser",),},),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None,{"classes": ("wide",),"fields": ("phone_number", "password1", "password2"),},),
    )
    list_display = ("phone_number", "full_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "gender", 'auth_type', 'user_role')
    search_fields = ("phone_number", "full_name", "email")
    ordering = ("phone_number",)


@admin.register(models.Lawyer)
class LawyerAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("work_place", "bio")}),
        (_("User choices"), {"fields": ('user', "license_status", "type", 'profession', 'consultation', 'language')}),
        (_("Personal Info"), {"fields": ("license_date", 'inter_expires_has', 'experience', 'card', 'consultation_price')}),
    )
    list_display = ('id', "user", "work_place", "type")
    list_filter = ("type",)


@admin.register(models.UserConformation)
class UserConformationAdmin(admin.ModelAdmin):
    list_display = ('code','user','expires','is_used','code_type')
    list_filter = ('expires','is_used','code_type')


@admin.register(models.Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name', )


@admin.register(models.LawyerRate)
class LawyerRateAdmin(admin.ModelAdmin):
    list_display = ('user','rate','comment')
    list_filter = ('rate','comment')
    search_fields = ('comment', )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'extra_phone']


@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    inlines = [RegionInline]
    def has_module_permission(self, request):
        return False


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    inlines = [CityInline]


@admin.register(models.Language)
class LanguageAdmin(admin.ModelAdmin):
    pass
