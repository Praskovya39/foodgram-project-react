# Generated by Django 3.2 on 2023-05-27 16:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recipes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcart',
            name='user',
            field=models.ForeignKey(help_text='Владелец корзины', on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL, verbose_name='Юзер'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(help_text='Разместивший рецепты', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор рецепта'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredient',
            field=models.ManyToManyField(help_text='выберите ингридиенты, необходимые для приготовления', related_name='recipes', through='recipes.IngredientsInRecipe', to='recipes.Ingredient', verbose_name='Ингридиенты'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(help_text='Выберите теги', related_name='recipes', to='recipes.Tag', verbose_name='Тег'),
        ),
        migrations.AddField(
            model_name='ingredientsinrecipe',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_ingredients', to='recipes.ingredient'),
        ),
        migrations.AddField(
            model_name='ingredientsinrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_ingredients', to='recipes.recipe'),
        ),
        migrations.AddField(
            model_name='favorites',
            name='recipe',
            field=models.ForeignKey(help_text='Понравившийся рецепт', on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AddField(
            model_name='favorites',
            name='user',
            field=models.ForeignKey(help_text='Тот, кто лайкает', on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='Юзер'),
        ),
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_cart'),
        ),
        migrations.AddConstraint(
            model_name='ingredientsinrecipe',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='unique_recipe'),
        ),
        migrations.AddConstraint(
            model_name='favorites',
            constraint=models.UniqueConstraint(fields=('recipe', 'user'), name='unique_favorites'),
        ),
    ]
