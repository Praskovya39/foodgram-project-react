from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from foodgram.settings import MIN_VALUE_MINUTES, MIN_VALUE_AMOUNT

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=64,
        blank=False,
        verbose_name='Название',
        help_text='Указать название'
    )
    measurement_unit = models.CharField(
        max_length=64,
        blank=False,
        verbose_name='Единицы измерения',
        help_text='Указать единицы измерения'
    )

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=64,
        unique=True,
        blank=False,
        verbose_name='Название',
        help_text='Указать название'
    )
    color = models.CharField(
        max_length=16,
        unique=True,
        blank=False,
        verbose_name='Цвет',
        help_text='Выбрать цвет'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        blank=False,
        verbose_name='Слаг тега',
        help_text='Указать слаг тега'
    )

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        max_length=200,
        blank=False,
        verbose_name='Название',
        help_text='Указать название'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Картинка',
        help_text='Фотография Вашего кулинарного изыска'
    )
    text = models.TextField(
        blank=False,
        verbose_name='Описание',
        help_text='Краткое описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientsInRecipe',
        related_name='recipes',
        verbose_name='Ингредиент'
    )
    cooking_time = models.PositiveSmallIntegerField(
        blank=False,
        verbose_name='Время приготовления',
        help_text='Указать время приготовления',
        validators=(
            MinValueValidator(
                MIN_VALUE_MINUTES,
                message=(f'Время менее {MIN_VALUE_MINUTES} мин')
            ),
        ),)
    tags = models.ManyToManyField(
        Tag,
        blank=False,
        related_name='recipes',
        verbose_name='Тег',
        help_text='Выберите теги'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        help_text='Разместивший рецепты'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class TagRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='tags',
        verbose_name='Тэг'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='tags_in_recipe',
        verbose_name='Рецепт',
    )

    def __str__(self):
        return f'{self.tag} рецепта {self.recipe}'

    class Meta:
        verbose_name = 'Тэг в рецепте'
        verbose_name_plural = 'Тэги в рецепте'


class IngredientsInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    amount = models.PositiveSmallIntegerField(
        blank=False,
        verbose_name='Количество',
        help_text='Указать количество',
        validators=(
            MinValueValidator(
                MIN_VALUE_AMOUNT,
                message=f'Ингридиентов не менее {MIN_VALUE_AMOUNT}',
            ),
        ),
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте',
        verbose_name_plural = 'Ингредиенты в рецепте',
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique_recipe'
            ),
        )


class Favorites(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Юзер',
        help_text='Тот, кто лайкает')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
        help_text='Понравившийся рецепт')

    class Meta:
        verbose_name = 'Избранное',
        verbose_name_plural = 'Избранное',
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'user'), name='unique_favorites'
            ),
        )

    def __str__(self):
        return f'{self.recipe} добавлено в избранное'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Юзер',
        help_text='Владелец корзины')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт',
        help_text='Рецепт, из которого берутся ингридиенты')

    class Meta:
        verbose_name = 'Корзина покупки',
        verbose_name_plural = 'Корзина покупок',
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_cart'),
        )

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в Корзину покупок'
