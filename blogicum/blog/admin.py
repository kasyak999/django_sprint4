from django.contrib import admin
from .models import Post, Category, Location, User, Comment
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.db.models import Q


class MainAdmin(admin.ModelAdmin):
    list_display_links = ('title',)
    list_filter = ('is_published',)
    search_fields = ['title']
    list_per_page = 10

    actions = ['on_published', 'off_published']  # Действие

    @admin.action(description="Опубликовать")
    def on_published(self, modeladmin, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description="Снять с публикации")
    def off_published(self, modeladmin, request, queryset):
        queryset.update(is_published=False)


class LocationAdmin(MainAdmin):
    list_display = (
        'id',
        'name',
        'is_published'
    )
    list_display_links = ('name',)
    list_filter = ('is_published',)
    search_fields = ['name']


class MyFilter(admin.SimpleListFilter):
    title = _('Видны на сайте')
    parameter_name = 'category__is_published'

    def lookups(self, request, model_admin):
        return (
            (True, _('Да')),
            (False, _('Нет')),
        )

    def queryset(self, request, queryset):
        value = request.GET.get(self.parameter_name)
        if value is not None:  # Проверяем, было ли выбрано значение
            if value == 'True':
                return queryset.filter(
                    category__is_published=True,
                    is_published=True
                )
            elif value == 'False':
                return queryset.filter(
                    Q(category__is_published=True) | Q(is_published=True)
                )
        return queryset


class PostAdmin(MainAdmin):
    list_display = (
        'id',
        'title',
        'is_published',
        'category',
    )
    list_filter = ('is_published', MyFilter)


class CategoryAdmin(MainAdmin):
    list_display = (
        'id',
        'title',
        'is_published',
    )


class UserCommentsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text',
        'is_published',
    )


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Comment, UserCommentsAdmin)


# Регистрация модели User с вашим настроенным UserAdmin
class ListUsers(UserAdmin):
    list_display = ('username', 'email', 'is_staff')
    list_filter = ('posts__title',)


admin.site.unregister(User)
admin.site.register(User, ListUsers)
