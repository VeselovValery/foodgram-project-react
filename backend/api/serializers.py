import re

from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from drf_base64.fields import Base64ImageField

from recipes.models import Ingredient, Tag, RecipeIngredient, Recipe
from users.models import Subscriptions

User = get_user_model()


class IsSubscribed:

    def get_is_subscribed(self, obj):
        try:
            user_subscribers = Subscriptions.objects.get(id=obj.id)
        except Subscriptions.DoesNotExist:
            return False
        if user_subscribers.authors.count():
            return True


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )

    def validate_username(self, value):
        if User.objects.filter(username=value).count():
            raise serializers.ValidationError(
                'Указанное имя пользователя уже существует.'
            )
        elif not re.match(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError(
                'В username используются запрещенные символы'
            )
        return value

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def to_representation(self, instance):
        return {
            'email': instance.email,
            'id': instance.id,
            'username': instance.username,
            'first_name': instance.first_name,
            'last_name': instance.last_name
        }


class UserGetSerializer(serializers.ModelSerializer, IsSubscribed):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class RecipeIngredientGetSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ('ingredient', 'amount')


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    # ingredient = serializers.PrimaryKeyRelatedField(
    #     queryset=Ingredient.objects.all()
    # )
    # ingredient = serializers.SerializerMethodField()
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')

    # def get_ingredient(self, obj):
    #     return Ingredient.objects.get(pk=obj.id)


class RecipeGetSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserGetSerializer(read_only=True)
    ingredients = RecipeIngredientGetSerializer(many=True, read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            # "is_favorited",
            # "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time"
        )


class RecipeCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = RecipeIngredientCreateSerializer(many=True)
    # is_favorited = serializers.SerializerMethodField()
    # is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Recipe
        fields = (
            "tags",
            "ingredients",
            # "is_favorited",
            # "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    # def get_is_favorited(self, recipe):
    #     current_user = self.context["request"].user
    #     if (
    #         self.context["request"].user.is_authenticated
    #         and Favorite.objects.filter(recipe=recipe,
    #                                     user=current_user).exists()
    #     ):
    #         return True
    #     return False
    #
    # def get_is_in_shopping_cart(self, recipe):
    #     current_user = self.context["request"].user
    #     if (
    #         self.context["request"].user.is_authenticated
    #         and ShoppingCart.objects.filter(recipe=recipe,
    #                                         user=current_user).exists()
    #     ):
    #         return True
    #     return False

    def add_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.get(pk=ingredient['id'])
            current_recipe_ingredient, status = (
                RecipeIngredient.objects.get_or_create(
                    ingredient=current_ingredient,
                    amount=ingredient['amount']
                )
            )
            recipe.ingredients.add(current_recipe_ingredient)

    def create(self, validated_data):
        author = self.context["request"].user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data, author=author)
        self.add_ingredients(ingredients, recipe)
        recipe.tags.set(tags)
        print(tags)
        return recipe

    def update(self, instance, validated_data):
        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
            instance.ingredients.clear()
            self.add_ingredients(ingredients, instance)
        if 'tags' in validated_data:
            instance.tags.set(validated_data.pop('tags'))
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeGetSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }).data


class UserLikeRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionsSerializer(serializers.ModelSerializer, IsSubscribed):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_recipes(self, obj):
        limit = self.context.get('request').GET.get('recipes_limit')
        if limit:
            return UserLikeRecipeSerializer(
                obj.recipe.all()[:int(limit)],
                many=True
            ).data
        return UserLikeRecipeSerializer(
            obj.recipe.all(),
            many=True
        ).data

    def get_recipes_count(self, obj):
        return obj.recipe.count()
