# Generated by Django 3.2 on 2023-05-16 19:10

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': ('Избранное',),
                'verbose_name_plural': ('Избранное',),
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Указать название', max_length=64, verbose_name='Название')),
                ('measurement_unit', models.CharField(help_text='Указать единицы измерения', max_length=64, verbose_name='Единицы измерения')),
            ],
            options={
                'verbose_name': 'Ингридиент',
                'verbose_name_plural': 'Ингридиенты',
                'ordering': ('-name',),
            },
        ),
        migrations.CreateModel(
            name='IngredientsInRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(help_text='Указать количество', validators=[django.core.validators.MinValueValidator(1, message='Ингридиентов не менее 1')], verbose_name='Количество')),
            ],
            options={
                'verbose_name': ('Ингредиент в рецепте',),
                'verbose_name_plural': ('Ингредиенты в рецепте',),
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Указать название', max_length=200, verbose_name='Название')),
                ('image', models.ImageField(help_text='Фотография Вашего кулинарного изыска', upload_to='recipes/images/', verbose_name='Картинка')),
                ('text', models.TextField(help_text='Краткое описание рецепта', verbose_name='Описание')),
                ('coking_time', models.PositiveSmallIntegerField(help_text='Указать время приготовления', validators=[django.core.validators.MinValueValidator(1, message='Время менее 1 мин')], verbose_name='Время приготовления')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Указать название', max_length=64, unique=True, verbose_name='Название')),
                ('color', models.CharField(help_text='Выбрать цвет', max_length=16, unique=True, verbose_name='Цвет')),
                ('slug', models.SlugField(help_text='Указать слаг тега', unique=True, verbose_name='Слаг тега')),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'Тэги',
                'ordering': ('-name',),
            },
        ),
        migrations.CreateModel(
            name='TagRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags_in_recipe', to='recipes.recipe', verbose_name='Рецепт')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='recipes.tag', verbose_name='Тэг')),
            ],
            options={
                'verbose_name': 'Тэг в рецепте',
                'verbose_name_plural': 'Тэги в рецепте',
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(help_text='Рецепт, из которого берутся ингридиенты', on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='recipes.recipe', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': ('Корзина покупки',),
                'verbose_name_plural': ('Корзина покупок',),
            },
        ),
    ]
