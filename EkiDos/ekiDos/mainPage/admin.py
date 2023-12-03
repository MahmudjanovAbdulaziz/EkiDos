from django.contrib import admin

from .models import *

@admin.register(FoodCategory)
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'anchor')
    search_fields = ('name', 'anchor')

# Регистрация модели Dish
@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')

admin.site.register(Comments)