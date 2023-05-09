from django.contrib import admin
from django.utils import timezone

from service_backend.models import User, Application, Friendship


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'password',
    )
    search_fields = ['username']


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'applicant',
        'created_at',
    )
    search_fields = ['user', 'applicant']


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user1',
        'user2',
    )
    search_fields = ['user', 'applicant']
