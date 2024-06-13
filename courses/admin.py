from django.contrib import admin
from .models import *


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')


class TaskOptionInline(admin.StackedInline):
    model = TaskOption
    max_num = 5
    extra = 0


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    inlines = [TaskOptionInline, ]


@admin.register(TaskOption)
class TaskOptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'title')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'answer_option', 'user')
