from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
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
        return f'{self.name} ({self.unit}.)'


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
        default=1,
        validators=(MinValueValidator(1),)
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient'
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
        return f'{self.name} от {self.author}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='amount'
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        default=1,
        validators=(MinValueValidator(
            1,
            message='Минимальное количество ингридиентов 1'),)
        )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Количество ингредиента'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_amount_ingredient'
            )
        ]

    def __str__(self):
        return (f'В рецепте {self.recipe.name} содержиться '
                f'{self.ingredient} - {self.amount}')


class UserLikeRecipe(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='like_recipe'
    )
    recipes = models.ManyToManyField(
        Recipe,
        verbose_name='Избранный рецепт',
        related_name='like_recipe'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Избранный рецепт'

    def __str__(self):
        list_recipes = [
            recipe['name'] for recipe in self.recipes.values('name')
        ]
        return (f'Пользователь {self.user} добавил рецепты: '
                f'{"".join(list_recipes)} в избранное')


class UserShoppingCard(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='shopping_card'
    )
    recipes = models.ManyToManyField(
        Recipe,
        verbose_name='Рецепты для список покупок',
        related_name='shopping_card'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Список покупок'

    def __str__(self):
        list_recipes = [
            recipe['name'] for recipe in self.recipes.values('name')
        ]
        return (f'Пользователь {self.user} добавил рецепты: '
                f'{"".join(list_recipes)} в покупки')
