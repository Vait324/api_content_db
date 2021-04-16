from django.contrib import admin

from .models import Categories, Comment, CustomUser, Genres, Review, Titles


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'email', 'bio', 'role'
    )
    list_filter = ('role',)
    empty_value_display = '-пусто-'
    model = CustomUser


class CommentInLine(admin.StackedInline):
    model = Comment


class GenresInLine(admin.StackedInline):
    model = Genres


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'title', 'text', 'author', 'score', 'pub_date'
    )
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
    inlines = [CommentInLine]


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'slug'
    )
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    empty_value_display = '-пусто-'


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'slug'
    )
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    empty_value_display = '-пусто-'


@admin.register(Titles)
class TitlesAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'year', 'description'
    )
    list_filter = ('year',)
    empty_value_display = '-пусто-'
