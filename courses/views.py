from django.contrib.auth import login as login_user, logout as logout_user
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from config import settings
from courses.models import Course, Task


def index(request):
    return render(request, 'main/index.html')


@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            login_user(request, user)
            return redirect('index')
        else:
            return render(request, 'main/login.html', context=dict(error='Неверный email или пароль'))

    return render(request, 'main/login.html')


@csrf_exempt
def logout(request):
    if request.user.is_authenticated:
        logout_user(request)
    return redirect('index')


@csrf_exempt
def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        password_again = request.POST['password_again']

        user = User.objects.filter(email=email).first()
        if user:
            return render(request, 'main/login.html',
                          context=dict(error='Пользователь с данным email уже зарегистрирован'))
        elif password != password_again:
            return render(request, 'main/login.html',
                          context=dict(error='Пароли не совпадают'))
        else:
            user = User.objects.create_user(email=email, password=password)
            login_user(request, user)
            return redirect('index')

    return render(request, 'main/register.html')


def courses_list(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'courses/list.html', context=dict(
        MEDIA_URL=settings.MEDIA_URL,
        courses=Course.objects.filter(tasks__isnull=False).distinct().all()
    ))


def course_item(request, course_id, task_id=None):
    if not request.user.is_authenticated:
        return redirect('login')

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

    selected_task = selected_task or tasks[0]

    return render(request, 'courses/item.html', context=dict(
        MEDIA_URL=settings.MEDIA_URL,
        course=course,
        tasks=tasks,
        selected_task=selected_task,
        selected_task_number=selected_task_number or 1,
        options=list(map(lambda x: {
            'title': str(x),
            'id': x.id,
            'checked': x.checked(request.user),
        }, selected_task.options.all()))
    ))
