from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,UserDetail


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('__str__','is_active','id',)
    list_filter = ('email',)
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        ("Field",{'fields':("email","password")}),
        ("permission",{'fields':("is_active","is_staff","is_superuser")})
    )
    add_fieldsets = (
        ("Add_User",{
            "fields":("email","password1","password2","is_staff")}),
    )
# Register your models here.


admin.site.register(UserDetail)