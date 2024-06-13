import uuid

from django.contrib.auth.models import User
from django.db import models


def course_storage(instance, filename):
    ext = filename.split(".")[-1]
    uuid_filename = "{}.{}".format(uuid.uuid4(), ext)
    return 'media/course_storage/{0}'.format(uuid_filename)


class Course(models.Model):
    title = models.CharField(max_length=256, verbose_name="Название")
    description = models.TextField(default="", verbose_name="Описание")

    image = models.ImageField(upload_to=course_storage, verbose_name="Изображение", null=True)

    min_tasks_for_pass = models.IntegerField(verbose_name="Мин. Кол-во задач для прохождения", default=0)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Task(models.Model):
    course = models.ForeignKey(Course, related_name="tasks", on_delete=models.CASCADE, verbose_name="Курс")

    title = models.CharField(max_length=256, verbose_name="Название")

    number = models.IntegerField(verbose_name="Позиция", default=0)

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"

    def __str__(self):
        return self.title


class TaskOption(models.Model):
    task = models.ForeignKey(Task, related_name="options", on_delete=models.CASCADE, verbose_name="Задание")

    title = models.CharField(max_length=256, verbose_name="Название")

    correctly = models.BooleanField(default=False, verbose_name="correctly")

    class Meta:
        verbose_name = "Вариант ответа на задание"
        verbose_name_plural = "Варианты ответов на задания"

    def __str__(self):
        return self.title

    def checked(self, user) -> bool:
        return bool(Answer.objects.filter(answer_option=self, user=user).first())


class AnswerStatus(models.IntegerChoices):
    ON_CHECK = 0, "На проверке"
    NOT_PASSED = 1, "Не пройдено"
    PASSED = 2, "Пройдено"


class Answer(models.Model):
    user = models.ForeignKey(User, related_name='answers', on_delete=models.CASCADE, verbose_name="Пользователь")

    task = models.ForeignKey(Task, related_name='answers', on_delete=models.CASCADE, verbose_name="Задание")

    status = models.IntegerField(choices=AnswerStatus.choices, default=AnswerStatus.ON_CHECK,
                                 verbose_name="Тип услуги")

    answer_option = models.ForeignKey(TaskOption, related_name="answers", on_delete=models.CASCADE,
                                      verbose_name="Вариант ответа на задание")

    class Meta:
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "Ответы пользователей"
