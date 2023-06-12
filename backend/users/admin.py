from django.contrib import admin

from .models import User, Follow


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_admin')
    search_fields = ('username', 'email')
    list_filter = ('is_admin')
    ordering = ('username', )
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    search_fields = ('user__username', 'user__email',
                     'author__username', 'author__email')
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
