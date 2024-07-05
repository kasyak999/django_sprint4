from django.contrib import admin
from .models import Post, Category, Location, User
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
    def on_published(modeladmin, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description="Снять с публикации")
    def off_published(modeladmin, request, queryset):
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
    title = _('Видны на сайте')  # Имя, которое будет отображаться в админ-панели
    parameter_name = 'category__is_published'  # Название параметра URL для фильтра

    def lookups(self, request, model_admin):
        return (
            (True, _('Да')),
            (False, _('Нет')),
        )

    def queryset(self, request, queryset):
        value = request.GET.get(self.parameter_name)  # Получаем значение фильтра из URL
        if value is not None:  # Проверяем, было ли выбрано значение
            if value == 'True':  # Если значение 'True', то фильтруем по 'is_published=True'
                return queryset.filter(
                    category__is_published=True,
                    is_published=True
                )
            elif value == 'False':  # Если значение 'False', то фильтруем по 'is_published=False'
                # return queryset.filter(category__is_published=False)
                return queryset.filter(
                    Q(category__is_published=True) | Q(is_published=True)
                )
        return queryset  # Возвращаем весь набор данных, если значение фильтра не задано


class PostAdmin(MainAdmin):
    list_display = (
        'id',
        'title',
        'is_published',
        'category',
    )
    # list_editable = ('is_published',)
    list_filter = ('is_published', MyFilter)


class CategoryAdmin(MainAdmin):
    list_display = (
        'id',
        'title',
        'is_published',
    )


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)


# Регистрация модели User с вашим настроенным UserAdmin
class ListUsers(UserAdmin):
    list_display = ('username', 'email', 'is_staff')
    list_filter = ('posts__title',)


admin.site.unregister(User)
admin.site.register(User, ListUsers)
