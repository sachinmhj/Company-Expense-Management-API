from django.contrib import admin
from .models import User, ExpenseClaim, ExpenseCategory
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

# Register your models here.
@admin.register(User)
class UzerAdmin(UserAdmin):
    fieldsets = None
    fieldsets = (
        (None, {"fields": ("username", "password", "role", "supervisor")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

admin.site.register(ExpenseClaim)
admin.site.register(ExpenseCategory)