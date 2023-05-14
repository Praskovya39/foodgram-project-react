from django.contrib import admin
from recipes.models import (Ingredient, Tag, Recipe,
                            IngredientsInRecipe, Favorites, ShoppingCart)


class IngredientAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):

    list_display = ('id', 'color', 'slug')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class RecipeAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'image', 'text', 'coking_time', 'author')
    search_fields = ('name',)
    list_filter = ('name', 'author__username', 'tags',)
    empty_value_display = '-пусто-'

    @admin.display(description='В избранном')
    def favorites_count(self, obj):
        return obj.favorites.count()


class IngredientsInRecipeAdmin(admin.ModelAdmin):

    list_display = ('ingredient', 'recipe', 'amount')
    empty_value_display = '-пусто-'


class FavoritesAdmin(admin.ModelAdmin):

    list_display = ('user', 'recipe')
    empty_value_display = '-пусто-'


class ShoppingCartAdmin(admin.ModelAdmin):

    list_display = ('user', 'recipe')
    empty_value_display = '-пусто-'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientsInRecipe, IngredientsInRecipeAdmin)
admin.site.register(Favorites, FavoritesAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
