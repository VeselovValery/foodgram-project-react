from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Follow

EMPTY_FILLING = '-пусто-'

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'password',
        'email',
        'first_name',
        'last_name',
        'role'
    )
    list_editable = ('username',)
    search_fields = ('email', 'username')
    list_filter = ('email', 'username')
    empty_value_display = EMPTY_FILLING


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'following')
    search_fields = ('author__username', 'following__username')
    list_filter = ('author__username', 'following__username')
    empty_value_display = EMPTY_FILLING
