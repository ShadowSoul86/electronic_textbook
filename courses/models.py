from django.contrib.auth.models import User
from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=256, verbose_name="Название")
    description = models.TextField(default="", verbose_name="Описание")

    tasks = models.TextField(default="", verbose_name="Задачи")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Task(models.Model):
    course = models.ForeignKey(Course, related_name="tasks", on_delete=models.CASCADE, verbose_name="Курс")

    title = models.CharField(max_length=256, verbose_name="Название")
    description = models.TextField(default="", verbose_name="Описание")

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"

    def __str__(self):
        return self.title


class Answer(models.Model):
    answer_body = models.TextField(default="", verbose_name="Тело ответа")

    user = models.ForeignKey(User, related_name='answers', on_delete=models.CASCADE, verbose_name="Пользователь")

    class Meta:
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "Ответы пользователей"
