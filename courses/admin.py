from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
from django.urls import reverse


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    fields = ('id', 'title', 'number', 'task_link',)
    readonly_fields = ('task_link',)

    def task_link(self, obj):
        if obj.id is not None:
            url = reverse("admin:courses_task_change", args=[obj.id])
            link = '<a href="%s">Редактор задания</a>' % url
            return mark_safe(link)
        else:
            return mark_safe('Нажмите <b>"Сохранить и продолжить редактирование"</b> для редактирования')

    task_link.short_description = 'Ссылка на задание'

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('number')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    model = Course
    list_display = ('id', 'title', 'description')
    inlines = (TaskInline,)


class TaskOptionInline(admin.StackedInline):
    model = TaskOption
    extra = 0
    fields = ('id', 'title', 'correctly', 'task_link',)
    readonly_fields = ('task_link',)

    def task_link(self, obj):
        if obj.id is not None:
            url = reverse("admin:courses_taskoption_change", args=[obj.id])
            link = '<a href="%s">Редактор варианта ответа</a>' % url
            return mark_safe(link)
        else:
            return mark_safe('Нажмите <b>"Сохранить и продолжить редактирование"</b> для редактирования')

    task_link.short_description = 'Ссылка на вариант ответа'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    inlines = [TaskOptionInline, ]


@admin.register(TaskOption)
class TaskOptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'title')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'answer_option', 'user', 'status')
    readonly_fields = ('status',)

    def status(self, obj):
        return 'Верно' if obj.correctly else 'Неверно'

    status.short_description = "Статус"
