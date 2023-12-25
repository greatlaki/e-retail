from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user.models import User


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for user"""

    ordering = ['id']
    list_display = ['email', 'is_active']
    list_filter = (
        'email',
        'is_active',
        'is_staff',
    )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                )
            },
        ),
        ('Profile', {'fields': ('first_name', 'last_name')}),
        ('Important dates', {'fields': ('last_login',)}),
        ('Employer', {'fields': ('employer',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'is_active',
                    'is_staff',
                ),
            },
        ),
    )
    search_fields = ('email',)


admin.site.register(User, UserAdmin)
