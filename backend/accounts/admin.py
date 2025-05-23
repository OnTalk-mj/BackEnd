from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'email', 'name', 'birth', 'phone', 'is_staff')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('email', 'name')
    ordering = ('id',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('개인정보', {'fields': ('name', 'birth', 'phone', 'address', 'zipcode')}),
        ('권한', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    # user 대신 email 사용
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

admin.site.register(User, UserAdmin)
