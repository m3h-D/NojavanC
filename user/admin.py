from django.contrib import admin
from .models import Group, User, Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import RegisterForm, UserChangeForm

class ProfileInline(admin.StackedInline):
    model = Profile
    # bayraye inke in inja kar kone, bayad tu Schedule search filedesh kar kone!
    autocomplete_fields = ['user']
    extra = 0


class UserAdmin(BaseUserAdmin):
    """The forms to add and change user instances
    
    Arguments:
        BaseUserAdmin {MODULE} -- a built-in django Admin

    """
    form = UserChangeForm
    add_form = RegisterForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('phone', 'get_name', 'sex', 'id')
    # list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'password', 'username')}),
        ('Personal info', {'fields': (('first_name', 'last_name'), 'sex')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'is_staff', 'is_compeleted', 'user_permissions')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'password')}
         ),
    )
    search_fields = ('phone', 'first_name', 'last_name', 'email', 'id')

    ordering = ('-id',)
    filter_horizontal = ()
    inlines = (ProfileInline,)
    def get_name(self, obj):
        """full name of every user
        
        Arguments:
            obj {OBJECT} -- all instances of User Model
        
        Returns:
            STRING -- returns string of first_name and last_name
        """
        name = f'{obj.first_name} {obj.last_name}'
        return " ".join(name)

admin.site.register(User, UserAdmin)
admin.site.register(Group)
# Register your models here.
