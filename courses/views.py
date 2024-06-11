from django.db.models import Q
from django.shortcuts import render, redirect

from config import settings
from courses.models import Course, Task


def index(request):
    return render(request, 'main/index.html')


def courses_list(request):
    return render(request, 'courses/list.html', context=dict(
        MEDIA_URL=settings.MEDIA_URL,
        courses=Course.objects.filter(tasks__isnull=False).all()
    ))


def course_item(request, course_id, task_id=None):
    course = Course.objects.get(pk=course_id)

    tasks = Task.objects.filter(course=course).order_by('number').all()

    if not tasks:
        return redirect('index')

    selected_task = None
    selected_task_number = None

    for n, task in enumerate(tasks):
        if str(task.pk) == str(task_id):
            selected_task = task
            selected_task_number = n + 1
            break

    print(tasks)
    print(selected_task, selected_task_number)

    return render(request, 'courses/item.html', context=dict(
        MEDIA_URL=settings.MEDIA_URL,
        course=course,
        tasks=tasks,
        selected_task=selected_task or tasks[0],
        selected_task_number=selected_task_number or 1
    ))
