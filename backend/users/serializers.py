from django.shortcuts import get_object_or_404
from rest_framework import status, serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Recipe
from users.models import Subscription, CustomUser


class CustomUserListSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'id', 'email', 'username', 'first_name',
            'last_name', 'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscription.objects.filter(user=user, author=obj).exists()


class CustomUserPostSerializer(UserCreateSerializer):

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class RecipeProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count',
        )
        read_only_fields = ('email', 'username', 'first_name', 'last_name')

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.GET.get('recipes_limit')
        recipes = Recipe.objects.filter(author=obj.author)
        if recipes_limit:
            recipes = recipes[: int(recipes_limit)]
        serializer = RecipeProfileSerializer(recipes,
                                             many=True, read_only=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()

    def get_is_subscribed(self, obj):
        return True

    def validate(self, data):
        author_id = self.context.get(
            'request').parser_context.get('kwargs').get('id')
        author = get_object_or_404(CustomUser, id=author_id)
        user = self.context.get('request').user
        if Subscription.objects.filter(author=author, user=user).exists():
            raise serializers.ValidationError(
                detail='Подписка уже существует',
                code=status.HTTP_400_BAD_REQUEST,
            )
        if user == author:
            raise serializers.ValidationError(
                detail='Нельзя подписаться на самого себя',
                code=status.HTTP_400_BAD_REQUEST,
            )
        return data
