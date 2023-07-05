from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    # list_display = ('username',)
    # def get_inline_instances(self, request, obj=None):
    #     if not obj:
    #         return list('status',)
    #     return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register your models here.
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'status')
# admin.site.register(Profile, ProfileAdmin)