from django.contrib import admin
from users.models import User


class RecipeAdmin(admin.ModelAdmin):

    list_display = ('id', 'username', 'email', 'first_name',
                    'last_name', 'password')
    search_fields = ('username',)
    list_filter = ('username', 'email',)
    empty_value_display = '-пусто-'


admin.site.register(User)