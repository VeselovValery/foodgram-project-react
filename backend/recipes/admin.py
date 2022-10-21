from django.contrib import admin

from .models import Ingredient, Tag, Recipe, RecipeIngredient, UserLikeRecipe

EMPTY_FILLING = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'unit')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = EMPTY_FILLING


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    list_display_links = ('name',)
    search_fields = ('name',)
    empty_value_display = EMPTY_FILLING


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'name',
        'image',
        'text',
        'cooking_time',
        'get_ingredients',
        'get_tags',
        'pub_date'
    )
    list_display_links = ('name',)
    search_fields = ('author__username', 'name', 'tags')
    list_filter = ('author__username', 'name', 'tags')
    empty_value_display = EMPTY_FILLING

    @admin.display(description='Ингредиенты')
    def get_ingredients(self, obj):
        list_ingredients = [
            ingredient.ingredient.name for ingredient in obj.ingredients.all()
        ]
        return ', '.join(list_ingredients)

    @admin.display(description='Тэги')
    def get_tags(self, obj):
        list_tags = [tag.name for tag in obj.tags.all()]
        return ', '.join(list_tags)


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'ingredient', 'amount')
    list_display_links = ('ingredient',)
    search_fields = ('ingredient__name',)
    list_filter = ('ingredient__name',)
    empty_value_display = EMPTY_FILLING


@admin.register(UserLikeRecipe)
class UserLikeRecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'get_recipes')
    list_display_links = ('user',)
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = EMPTY_FILLING

    @admin.display(description='Рецепты')
    def get_recipes(self, obj):
        list_recipes = [recipe.name for recipe in obj.recipes.all()]
        return ', '.join(list_recipes)
