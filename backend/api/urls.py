from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    TagViewSet,
    IngredientViewSet,
    RecipesViewSet,
    UserLikeRecipeView,
    SubscriptionsView,
    SubscribeView,
    UserShoppingCardView,
    download_shopping_cart
)

app_name = 'api'

router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipesViewSet)
urlpatterns = [
    path('recipes/<int:recipe_id>/favorite/', UserLikeRecipeView.as_view()),
    path(
        'recipes/<int:recipe_id>/shopping_cart/',
        UserShoppingCardView.as_view()
    ),
    path('recipes/download_shopping_cart/', download_shopping_cart),
    path('users/subscriptions/', SubscriptionsView.as_view()),
    path('users/<int:author_id>/subscribe/', SubscribeView.as_view()),
    path('', include(router.urls)),
    path(r'', include('djoser.urls')),
    path(r'auth/', include('djoser.urls.authtoken')),
]
