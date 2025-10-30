from django.db import models


class BlogPost(models.Model):
    objects = None
    title = models.CharField(
        max_length=300,
        verbose_name='Заголовок'
    )
    content = models.TextField(
        verbose_name='Содержимое'
    )
    preview = models.ImageField(
        verbose_name='Превью (изображение)'
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания'
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name='Опубликовано'
    )
    views = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество просмотров'
    )

    class Meta:
        verbose_name = 'Блоговая запись'
        verbose_name_plural = 'Блоговые записи'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
