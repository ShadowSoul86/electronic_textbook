from django.contrib.auth.models import User
from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=256, verbose_name="Название")
    description = models.TextField(default="", verbose_name="Описание")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Task(models.Model):
    course = models.ForeignKey(Course, related_name="tasks", on_delete=models.CASCADE, verbose_name="Курс")

    title = models.CharField(max_length=256, verbose_name="Название")
    description = models.TextField(default="", verbose_name="Описание")

    min_tasks_for_pass = models.IntegerField(verbose_name="Мин. Кол-во задач для прохождения", default=0)

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"

    def __str__(self):
        return self.title


class AnswerStatus(models.IntegerChoices):
    ON_CHECK = 0, "На проверке"
    NOT_PASSED = 1, "Не пройдено"
    PASSED = 2, "Пройдено"


class Answer(models.Model):
    answer_body = models.TextField(default="", verbose_name="Тело ответа")

    user = models.ForeignKey(User, related_name='answers', on_delete=models.CASCADE, verbose_name="Пользователь")

    task = models.ForeignKey(Task, related_name='answers', on_delete=models.CASCADE, verbose_name="Задание")

    status = models.IntegerField(choices=AnswerStatus.choices, default=AnswerStatus.ON_CHECK,
                                 verbose_name="Тип услуги")

    class Meta:
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "Ответы пользователей"
