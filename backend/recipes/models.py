from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Ингредиент',
        max_length=255
    )
    unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=255
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'

    def __str__(self):
        return f'{self.name}, {self.unit}.'


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Тег',
        max_length=255,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        unique=True
    )
    slug = models.SlugField(
        verbose_name='Словарный идентификатор',
        max_length=255,
        unique=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тэг'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор'
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=255
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='static/recipe/',
        blank=True,
        null=True
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        default=1
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'

    def __str__(self):
        return f'{self.name}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='amount_ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_for_recipe')
    amount = models.IntegerField(
        verbose_name='Количество',
        default=1
        )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Количество ингредиента'
