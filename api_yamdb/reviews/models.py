from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from constants import MIN_SCORE, MAX_SCORE


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Название произведения" 
    )
    text = models.TextField(verbose_name="Отзыв")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор"

    )
    score = models.IntegerField(
        verbose_name="Оценка",
        validators=[
            MinValueValidator(MIN_SCORE),
            MaxValueValidator(MAX_SCORE),
        ],
    )
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
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
        verbose_name="Автор"
    )
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )
