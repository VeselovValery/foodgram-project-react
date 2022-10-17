from django.contrib import admin

from .models import Ingredient, Tag, Recipe, RecipeIngredient

EMPTY_FILLING = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'unit')
    list_editable = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = EMPTY_FILLING


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    list_editable = ('name',)
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
    list_editable = ('name',)
    search_fields = ('author__username', 'name', 'tags')
    list_filter = ('author__username', 'name', 'tags')
    empty_value_display = EMPTY_FILLING

    @admin.display(description='Ингредиенты')
    def get_ingredients(self, obj):
        list_ingredients = [
            ingredient.name for ingredient in obj.ingredients.all()
        ]
        return ', '.join(list_ingredients)

    @admin.display(description='Тэги')
    def get_tags(self, obj):
        list_tags = [tag.name for tag in obj.tags.all()]
        return ', '.join(list_tags)


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount')
    search_fields = ('recipe__name', 'ingredient__name')
    list_filter = ('recipe__name', 'ingredient__name')
    empty_value_display = EMPTY_FILLING
