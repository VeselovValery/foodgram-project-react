from django.shortcuts import render
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework import filters, status
from rest_framework import generics, mixins, viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import pagination
# from rest_framework.pagination import LimitOffsetPagination
from djoser.views import UserViewSet

from recipes.models import Tag, Ingredient, Recipe, UserLikeRecipe
from users.models import Subscriptions
from .serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeGetSerializer,
    RecipeCreateSerializer,
    UserLikeRecipeSerializer,
    SubscriptionsSerializer
)

User = get_user_model()


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeGetSerializer
        return RecipeCreateSerializer


class UserLikeRecipeView(
    generics.CreateAPIView,
    generics.DestroyAPIView
):
    queryset = Recipe.objects.all()
    serializer_class = UserLikeRecipeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        like_recipe, created = UserLikeRecipe.objects.get_or_create(user=user)
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('recipe_id'))
        if like_recipe.recipes.filter(pk=recipe.pk).exists():
            return Response(
                {'errors': 'Этот рецепт уже есть в избранном у пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        like_recipe.recipes.add(recipe)
        serializer = self.get_serializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_object(self):
        like_recipe = get_object_or_404(UserLikeRecipe, user=self.request.user)
        return like_recipe

    def destroy(self, request, *args, **kwargs):
        recipe_id = self.kwargs.get('recipe_id')
        instance = self.get_object()
        if not instance.recipes.filter(pk=recipe_id).exists():
            return Response(
                {'errors': 'Данного рецепта нет в избранном у автора'},
                status=status.HTTP_400_BAD_REQUEST
            )
        recipe = get_object_or_404(Recipe, id=recipe_id)
        instance.recipes.remove(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionsView(generics.ListAPIView):
    serializer_class = SubscriptionsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        user_subscribers, created = Subscriptions.objects.get_or_create(
            user=user
        )
        return user_subscribers.authors.all()


class SubscribeView(
    generics.CreateAPIView,
    generics.DestroyAPIView
):
    queryset = User.objects.all()
    serializer_class = SubscriptionsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        user_subscribers, created = Subscriptions.objects.get_or_create(
            user=user
        )
        author = get_object_or_404(User, id=self.kwargs.get('author_id'))
        if author.id == user.id:
            return Response(
                {'errors': 'Нельзя подписаться на самого себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if user_subscribers.authors.filter(id=author.id).exists():
            return Response(
                {'errors': 'Подписка на данного автора уже сущестует'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user_subscribers.authors.add(author)
        serializer = self.get_serializer(author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_object(self):
        user_subscribers = get_object_or_404(
            Subscriptions,
            user=self.request.user
        )
        return user_subscribers

    def destroy(self, request, *args, **kwargs):
        author_id = self.kwargs.get('author_id')
        instance = self.get_object()
        if not instance.authors.filter(pk=author_id).exists():
            return Response(
                {'errors': 'Пользователь не подписан на этого автора'},
                status=status.HTTP_400_BAD_REQUEST
            )
        author = get_object_or_404(User, id=author_id)
        instance.authors.remove(author)
        return Response(status=status.HTTP_204_NO_CONTENT)
