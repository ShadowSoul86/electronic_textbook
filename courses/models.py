import uuid
from typing import Dict

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

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title

    def get_statistics(self, user) -> Dict:
        tasks_count = Task.objects.filter(course=self).count()
        tasks_answered = Answer.objects.filter(user=user, task__course=self).count()
        tasks_complete = Answer.objects.filter(user=user, task__course=self, answer_option__correctly=True).count()

        return dict(
            tasks_count=tasks_count,
            tasks_complete=tasks_complete,
            tasks_not_passed=tasks_answered - tasks_complete,
            tasks_no_answer=tasks_count - tasks_answered,
        )


def attachment_upload(instance, filename):
    return 'attachment_upload/{0}/{1}'.format(instance.course_id, filename)


class Task(models.Model):
    course = models.ForeignKey(Course, related_name="tasks", on_delete=models.CASCADE, verbose_name="Курс")

    title = models.CharField(max_length=256, verbose_name="Название")

    number = models.IntegerField(verbose_name="Позиция", default=0)

    file = models.FileField("Методический материал", upload_to=attachment_upload, blank=True, null=True)

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"

    def __str__(self):
        return self.title

    @property
    def next_task(self):
        return Task.objects.filter(course=self.course, number__gt=self.number).order_by('number').first()

    def get_user_answer(self, user):
        return Answer.objects.filter(user=user, task=self).first()


class TaskOption(models.Model):
    task = models.ForeignKey(Task, related_name="options", on_delete=models.CASCADE, verbose_name="Задание")

    title = models.CharField(max_length=256, verbose_name="Название")

    correctly = models.BooleanField(default=False, verbose_name="Корректный ответ")

    class Meta:
        verbose_name = "Вариант ответа на задание"
        verbose_name_plural = "Варианты ответов на задания"

    def __str__(self):
        return self.title

    def checked(self, user) -> bool:
        return Answer.objects.filter(answer_option=self, user=user).first()


class Answer(models.Model):
    user = models.ForeignKey(User, related_name='answers', on_delete=models.CASCADE, verbose_name="Пользователь")

    task = models.ForeignKey(Task, related_name='answers', on_delete=models.CASCADE, verbose_name="Задание")

    answer_option = models.ForeignKey(TaskOption, related_name="answers", on_delete=models.CASCADE,
                                      verbose_name="Вариант ответа на задание")

    class Meta:
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "Ответы пользователей"

    @property
    def correctly(self):
        return self.answer_option.correctly
