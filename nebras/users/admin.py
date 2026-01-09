from django.contrib import admin
from .models import Profile, Ban


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = ('user__username', 'user__email')

@admin.register(Ban)
class BanAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_banned', 'banned_start', 'banned_end', 'banned_by')
    list_filter = ('is_banned', 'banned_by')
    search_fields = ('user__username', 'reason')
