from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from rest_framework import filters
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from recipes.models import (Ingredient, Tag, Recipe, Favorites,
                            ShoppingCart, IngredientsInRecipe)
from api.serializers import (IngredientSerializer, TagSerializer,
                             RecipeSerializer, RecipeReadSerializer)
from api.filters import RecipesFilters
from foodgram.settings import LIST_DIR


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipesFilters
    ordering = ('-id',)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeSerializer

    @action(methods=['post', 'delete'],
            detail=True,
            permission_classes=[IsAuthenticated])
    def favorite(self, request):
        if request.method == 'POST':
            return self.create_obj(Favorites, request.user, pk)
        return self.delete_obj(Favorites, request.user, pk)

    @action(methods=['get', 'post', 'delete'],
            detail=True,
            permission_classes=[IsAuthenticated],
            url_path='shopping_cart')
    def shopping_cart(self, request):
        if request.method == 'POST':
            return self.create_obj(ShoppingCart, request.user, pk)
        elif request.method == 'GET':
            return self.download_shopping_cart(ShoppingCart, request.user)
        return self.delete_obj(ShoppingCart, request.user, pk)

    def create_obj(self, model, user, pk):
        if model.object.filter(user=user, recipe_id=pk).exists:
            return Response(
                {'message': 'Рецепт уже был добавлен'},
                status=status.HTTP_400_BAD_REQUEST
                )
        recipe = get_object_or_404(Recipe, id=pk)
        model.object.create(user=user, recipe=recipe)
        return Response(
            {'message': 'Рецепт добавлен'},
            status=status.HTTP_201_CREATED
            )

    def delete_obj(self, model, user, pk):
        obj = model.object.filter(user=user, recipe_id=pk)
        if obj.exists:
            obj.delete()
            return Response(
                {'message': 'Рецепт удален'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'message': 'Такой рецепт ранее не был добавлен'},
            status=status.HTTP_400_BAD_REQUEST
            )

    def download_shopping_cart(self, model):
        check_list = IngredientsInRecipe.objects.filter(
            recipe__cart__user=self.request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        with open(LIST_DIR, 'list.txt', 'a+') as list:
            list.write('check_list')
        filename = ({self.request.user.username}, 'list.xlsx')
        response = FileResponse(open(LIST_DIR + '/list.txt', 'rb'))
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
