import datetime
import textwrap as tw

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


def validate_year(value):
    if value > datetime.datetime.now().year:
        raise ValidationError(
            ('%(value)s больше текущего года. Введите корректный год'),
            params={'value': value},
        )


class Review(models.Model):
    title = models.ForeignKey(
        'Titles',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        null=False
    )
    text = models.TextField(
        max_length=500,
        help_text='Оставьте свой отзыв на произведение',
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
        null=False
    )
    score = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, 'Не меньше 1'),
            MaxValueValidator(10, 'Не больше 10')
        ],
        help_text='Поставьте произведению свою оценку',
        verbose_name='Оценка',
        null=False
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return tw.shorten(self.text, width=15, placeholder='...')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    title = models.ForeignKey(
        'Titles',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Произведение',
        null=False
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
        null=False
    )
    text = models.TextField(
        max_length=300,
        verbose_name='Комментарий',
        null=False
    )
    author = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
        null=False
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return tw.shorten(self.text, width=15, placeholder='...')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Categories(models.Model):
    name = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        verbose_name='Название категории',
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return tw.shorten(self.name, width=15, placeholder='...')

    class Meta:
        ordering = ('id',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genres(models.Model):
    name = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        verbose_name='Название жанра',
    )
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return tw.shorten(self.name, width=15, placeholder='...')


class Titles(models.Model):
    name = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        verbose_name='Название произведения',
    )
    year = models.IntegerField(
        default=0,
        validators=[validate_year],
        verbose_name='Год выпуска произведения',
    )
    description = models.CharField(
        max_length=200, null=True,
        verbose_name='Описание произведения',
    )
    genre = models.ManyToManyField(
        Genres, blank=True,
        related_name='item_genre'
    )
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL,
        null=True, related_name='item_category'
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return tw.shorten(self.name, width=15, placeholder='...')


class CustomUser(AbstractUser):

    class Role(models.TextChoices):
        USER = 'user', 'user'
        MODERATOR = 'moderator', 'moderator'
        ADMIN = 'admin', 'admin'

    role = models.CharField(
        choices=Role.choices,
        max_length=50,
        verbose_name='Роль пользователя',
        default=Role.USER,

    )
    email = models.EmailField(
        verbose_name='Email',
        help_text='Введите адрес эл.почты',
        unique=True
    )
    bio = models.TextField(
        verbose_name='О пользователе',
        help_text='Расскажите о себе',
        null=True
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    def __str__(self):
        return tw.shorten(self.email, width=15, placeholder='...')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
