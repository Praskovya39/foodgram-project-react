import base64

import webcolors
from django.db import transaction
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from recipes.models import (Ingredient, Tag,
                            Recipe, Favorites,
                            IngredientsInRecipe,
                            ShoppingCart, TagRecipe)
from foodgram.settings import (MIN_VALUE_MINUTES,
                               MIN_VALUE_AMOUNT,
                               MIN_VALUE_INGREDIENTS)
from api.errors import Error


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise Error.EMPTY_NAME
        return data


class TagSerializer(serializers.ModelSerializer):
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = '__all__'


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class IngredientsInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        read_only=True
    )
    name = serializers.SlugRelatedField(
        source='ingredient',
        slug_field='name',
        read_only=True,
    )
    measurement_unit = serializers.SlugRelatedField(
        source='ingredient',
        slug_field='measurement_unit',
        read_only=True,
    )

    class Meta:
        model = IngredientsInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class IngredientsInRecipeReadSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientsInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def validate_amount(self, amount):
        if amount < MIN_VALUE_AMOUNT:
            raise Error.NO_AMOUNT
        return amount


class RecipeReadSerializer(serializers.ModelSerializer):
    ingredient = IngredientsInRecipeReadSerializer(many=True)
    tags = TagSerializer(many=True)
    is_favorited = serializers.SerializerMethodField(
        read_only=True,
        method_name='is_in_favorities')
    is_in_shopping_cart = serializers.SerializerMethodField(
        read_only=True,
        method_name='is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('name', 'image', 'text', 'coking_time',
                  'ingridient', 'tags', 'author',
                  'is_in_shopping_cart', 'is_favorited',)

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return Favorites.objects.filter(
            user=request.user, recipe__id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return Recipe.objects.filter(
            shopping_cart__user=request.user,
            id=obj.id
        ).exists()


class RecipeSerializer(serializers.ModelSerializer):
    ingredient = IngredientsInRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    author = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault())
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = ('name', 'image', 'text',
                  'coking_time', 'ingredient', 'tags', 'author',)

    def create(self, validated_data):
        ingredient = validated_data.pop('ingredient')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredient:
            id = ingredient.get('id')
            amount = ingredient.get('amount')
            ingredient_id = get_object_or_404(Ingredient, id=id)
            IngredientsInRecipe.objects.create(
                recipe=recipe, ingredient=ingredient_id, amount=amount
            )
        recipe.tags.set(tags)
        recipe.save()
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.coking_time = validated_data.get(
            'coking_time', instance.coking_time)
        instance.ingredient = validated_data.get(
            'ingredient', instance.ingredient)
        instance.tags = validated_data.get('tags', instance.tags)
        instance.save()
        return instance

    def validate_ingredients(self, value):
        ingredients = value.get('ingredient')
        if len(ingredients) < MIN_VALUE_INGREDIENTS:
            raise Error.NO_INGREDIENT
        if len(ingredients) > len(ingredients.id):
            raise Error.NO_COPY
        return value

    def validate_cooking_time(self, cooking_time):
        if cooking_time < MIN_VALUE_MINUTES:
            raise Error.NO_TIME
        return cooking_time


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')
