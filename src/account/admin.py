from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import UsedResetToken, User, Profile, NewsletterSubscriber
from .forms import UserRegisterForm


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    # form = UserUpdateForm
    add_form = UserRegisterForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display=('email', 'username', 'active',)
    list_filter = ('active','staff','admin',)
    search_fields=['email']
    fieldsets = (
        ('User', {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('admin','staff','active','verified_email',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
                'classes': ('wide',),
                'fields': ("email","username","password","password2",)
            }
        ),
    )
    ordering = ('email',)
    filter_horizontal = ()




@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'username', 'account_type', 'approved', 'phone',)
    search_fields = ('fullname', 'address', 'state', 'city','zip',)
    list_filter = ('account_type', 'approved', 'state',)
    ordering = ('-created',)
    



admin.site.register(User, UserAdmin)
admin.site.register([NewsletterSubscriber, UsedResetToken])