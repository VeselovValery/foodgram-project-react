import django_filters as filters
from django.contrib.auth import get_user_model
from recipes.models import Recipe, Tag

User = get_user_model()


class RecipeFilter(filters.FilterSet):
    author = filters.CharFilter()
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        label='Tags',
        to_field_name='slug'
    )
    is_favorited = filters.BooleanFilter(method='get_is_favorite')
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('tags', 'author')

    def get_is_favorite(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(like_recipe__user=user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(shopping_card__user=user)
        return queryset
