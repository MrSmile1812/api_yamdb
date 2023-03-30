from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from constants import MIN_SCORE, MAX_SCORE


class Review(models.Model):
    text = models.TextField(verbose_name="Текст отзыва")
    author = ...
    score = models.IntegerField(verbose_name="Оценка", 
    validators=[MinValueValidator(MIN_SCORE), MaxValueValidator(MAX_SCORE)])
    pub_date = models.DateTimeField("Дата добавления", auto_now_add=True, db_index=True)

class Comment(models.Model):
    text = models.TextField(verbose_name="Текст отзыва")
    author = ...
    pub_date = models.DateTimeField("Дата добавления", auto_now_add=True, db_index=True)
