from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Subscriptions

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
    list_display_links = ('username',)
    search_fields = ('email', 'username')
    list_filter = ('email', 'username')
    empty_value_display = EMPTY_FILLING


@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'get_authors')
    list_display_links = ('user',)
    search_fields = ('user__username',)
    list_filter = ('user__username',)
    empty_value_display = EMPTY_FILLING

    @admin.display(description='На кого подписан')
    def get_authors(self, obj):
        list_authors = [author.username for author in obj.authors.all()]
        return ', '.join(list_authors)
