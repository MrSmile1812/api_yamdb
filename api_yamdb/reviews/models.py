from datetime import date

from django.db import models

from user.models import User

from .validators import (
    MaxValueValidator,
    MinValueValidator,
    UnicodeCategoryOrGenreNameValidator,
)


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
    description = models.TextField("Описание", blank=True)
    genre = models.ForeignKey(
        Genre,
        verbose_name="Жанр",
        null=True,
        on_delete=models.SET_NULL,
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    MIN_SCORE = 1
    MAX_SCORE = 10
    text = models.TextField(verbose_name="Текст отзыва")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="Reviews"
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата добавления", auto_now_add=True, db_index=True
    )
    score = models.IntegerField(
        verbose_name="Оценка",
        validators=[
            MaxValueValidator(MAX_SCORE),
            MinValueValidator(MIN_SCORE),
        ],
    )


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        verbose_name="Дата добавления", auto_now_add=True, db_index=True
    )
