from datetime import date

from django.db import models

from reviews.constants import MAX_SCORE, MIN_SCORE, TEXT_LENGTH
from reviews.validators import (
    MaxValueValidator, MinValueValidator, UnicodeCategoryOrGenreNameValidator,
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
        db_index=True,
    )

    class Meta:
        ordering = ["-id"]

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
        db_index=True,
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    current_date = date.today().year

    name = models.CharField(
        verbose_name="Название произведения", max_length=256, db_index=True
    )
    year = models.IntegerField(
        verbose_name="Год выпуска",
        validators=[MaxValueValidator(current_date)],
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre, related_name="titles", verbose_name="жанр"
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return self.name


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
        error_messages={"validators": "Оценка от 1 до 10!"},
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата добавления", auto_now_add=True, db_index=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "title",
                    "author",
                ),
                name="uq_author_title",
            )
        ]
        ordering = ["-id"]

    def __str__(self):
        return self.text[:TEXT_LENGTH]


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

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.text[:TEXT_LENGTH]
