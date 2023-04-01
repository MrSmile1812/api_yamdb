from datetime import date

from django.db import models

from reviews.constants import MAX_SCORE, MIN_SCORE
from reviews.validators import (
    MaxValueValidator,
    MinValueValidator,
    UnicodeCategoryOrGenreNameValidator,
)
from user.models import User


class Category(models.Model):
    name = models.CharField(
        verbose_name="Название категории",
        max_length=256,
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        validators=[UnicodeCategoryOrGenreNameValidator],
    )

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name="Название жанра",
        max_length=256,
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        validators=[UnicodeCategoryOrGenreNameValidator],
    )

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    current_date = date.today().year

    name = models.CharField(
        verbose_name="Название произведения",
        max_length=256,
    )
    year = models.IntegerField(
        verbose_name="Год выпуска",
        validators=[MaxValueValidator(current_date)],
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        null=True,
        on_delete=models.SET_NULL,
    )
    description = models.TextField("Описание", blank=True)
    genre = models.ManyToManyField(
        Genre,
        through="GenreTitle",
    )
    rating = 1

    def __str__(self) -> str:
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title, verbose_name="Произведение", on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genre,
        verbose_name="Жанр",
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return f"{self.genre} {self.title}"


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Название произведения",
    )
    text = models.TextField(verbose_name="Отзыв")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="Reviews",
        verbose_name="Автор",
    )
    score = models.IntegerField(
        verbose_name="Оценка",
        validators=[
            MaxValueValidator(MAX_SCORE),
            MinValueValidator(MIN_SCORE),
        ],
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата добавления", auto_now_add=True, db_index=True
    )


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name="Отзыв",
        related_name="comments",
    )
    text = models.TextField(verbose_name="Комментарий")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор",
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата добавления", auto_now_add=True, db_index=True
    )
