from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Token, Request, UsagePermission


class TokenAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'uuid']

    def user_email(self, obj: Token):
        return obj.user.email


admin.site.register(User)
admin.site.register(Request)
admin.site.register(UsagePermission)
admin.site.register(Token, TokenAdmin)
