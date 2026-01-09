from django.contrib import admin
from .models import MainSection, SubSection, SecondarySubSection

@admin.register(MainSection)
class MainSectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'order_index', 'created_by', 'created_at')
    search_fields = ('name',)

@admin.register(SubSection)
class SubSectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'main_section', 'order_index', 'created_by', 'created_at')
    list_filter = ('main_section',)
    search_fields = ('name',)

@admin.register(SecondarySubSection)
class SecondarySubSectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sub_section', 'order_index', 'created_by', 'created_at')
    list_filter = ('sub_section',)
    search_fields = ('name',)
