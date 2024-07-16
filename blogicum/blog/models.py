from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Count


User = get_user_model()
MAX_256 = 256
TITLE = 'Заголовок'
LINE_SLICE = 20


class DatabaseQueryManager(models.Manager):
    """Кастомный менеджер для фильтров"""

    def get_queryset(self):
        return super().get_queryset().filter(
            is_published=True,
            category__is_published=True,
            pub_date__lt=timezone.now()
        ).select_related(
            'author', 'category', 'location'
        ).annotate(comment_count=Count('comment')).order_by('-pub_date')


class PublishedModel(models.Model):
    """Базовая модель"""

    is_published = models.BooleanField(
        default=True, verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Добавлено'
    )

    class Meta:
        abstract = True
        ordering = ('created_at',)


class Category(PublishedModel):
    """Тематическая категория"""

    title = models.CharField(max_length=MAX_256, verbose_name=TITLE)
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True, verbose_name='Идентификатор',
        help_text=(
            "Идентификатор страницы для URL; разрешены символы латиницы, "
            "цифры, дефис и подчёркивание."
        )
    )

    class Meta(PublishedModel.Meta):
        """Перевод модели"""

        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        if len(self.title) > LINE_SLICE:
            result = self.title[:LINE_SLICE] + '...'
        else:
            result = self.title
        return result


class Location(PublishedModel):
    """Географическая метка"""

    name = models.CharField(max_length=MAX_256, verbose_name='Название места')

    class Meta(PublishedModel.Meta):
        """Перевод модели"""

        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        if len(self.name) > LINE_SLICE:
            result = self.name[:LINE_SLICE] + '...'
        else:
            result = self.name
        return result


class Post(PublishedModel):
    """Публикация"""

    image = models.ImageField(
        verbose_name='Фото', blank=True, upload_to='images'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        verbose_name='Местоположение',
        blank=True,
        on_delete=models.SET_NULL,
        null=True
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True
    )

    title = models.CharField(max_length=MAX_256, verbose_name=TITLE)
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            "Если установить дату и время в будущем — можно "
            "делать отложенные публикации."
        ),
        default=timezone.now
    )
    # objects = models.Manager()  # Менеджер по умолчанию
    # main_filter = DatabaseQueryManager()  # Кастомный менеджер

    class Meta(PublishedModel.Meta):
        """Перевод модели"""

        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)
        default_related_name = 'posts'

    def __str__(self):
        if len(self.title) > LINE_SLICE:
            result = self.title[:LINE_SLICE] + '...'
        else:
            result = self.title
        return result


class Comment(PublishedModel):  # UserComments
    """Коментарии"""

    text = models.TextField(verbose_name='Текст коментария')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta(PublishedModel.Meta):
        """Перевод модели"""

        verbose_name = 'коментарий'
        verbose_name_plural = 'Коментарии'
        default_related_name = "comment"

    def __str__(self):
        if len(self.text) > LINE_SLICE:
            result = self.text[:LINE_SLICE] + '...'
        else:
            result = self.text
        return result
