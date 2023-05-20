from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import CustomUserViewSet
from api.views import RecipeViewSet, IngredientViewSet, TagViewSet

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('recipes', RecipeViewSet)
router.register('ingredients', IngredientViewSet)
router.register('tags', TagViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
