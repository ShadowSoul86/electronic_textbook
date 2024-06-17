from django.contrib.auth import login as login_user, logout as logout_user
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from config import settings
from courses.models import Course, Task, TaskOption, Answer


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


def __post_register(request):
    email = request.POST['email']
    password = request.POST['password']
    password_again = request.POST['password_again']

    user = User.objects.filter(email=email).first()
    if user:
        return render(request, 'main/register.html',
                      context=dict(error='Пользователь с данным email уже зарегистрирован'))
    elif password != password_again:
        return render(request, 'main/register.html',
                      context=dict(error='Пароли не совпадают'))
    else:
        user = User.objects.create_user(email=email, password=password)
        login_user(request, user)
        return redirect('index')


@csrf_exempt
def register(request):
    if request.method == 'POST':
        return __post_register(request)
    return render(request, 'main/register.html')


def courses_list(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'courses/list.html', context=dict(
        MEDIA_URL=settings.MEDIA_URL,
        courses=[
            {
                'id': course.id,
                'title': course.title,
                'description': course.description,
                'image': course.image,
                **course.get_statistics(request.user)
            } for course in Course.objects.all() if course.tasks
        ]
    ))


def __post___course_item(request, course_id):
    task = Task.objects.get(pk=request.POST['task'], course_id=course_id)
    option = TaskOption.objects.get(pk=request.POST['option'])

    try:
        answer = Answer.objects.get(task=task, user=request.user)
        answer.answer_option = option
    except Answer.DoesNotExist:
        answer = Answer.objects.create(task=task, user=request.user, answer_option=option)
    answer.save()

    if next_task := task.next_task:
        return redirect('course_item', course_id=course_id, task_id=next_task.id)
    else:
        if request.POST.get('go_again') is not None:
            Answer.objects.filter(task__course_id=course_id, user=request.user).delete()
            return redirect('course_item', course_id=course_id)
        elif request.POST.get('go_to_courses') is not None:
            return redirect('courses_list')
        return redirect('course_item', course_id=course_id, task_id=task.id)


@csrf_exempt
def course_item(request, course_id, task_id=None):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        return __post___course_item(request, course_id)

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
        CURRENT_DOMAIN=settings.CURRENT_DOMAIN,
        MEDIA_URL=settings.MEDIA_URL,
        course=course,
        tasks=[{
            'id': task.id,
            'user_answer': task.get_user_answer(request.user),
        } for task in tasks],
        selected_task=selected_task,
        selected_task_number=selected_task_number or 1,
        options=list(map(lambda x: {
            'title': str(x),
            'id': x.id,
            'checked': x.checked(request.user),
        }, selected_task.options.order_by('?').all())),
        **course.get_statistics(request.user)
    ))


def lectures_list(request):
    return render(request, 'courses/lectures.html', context=dict(
        CURRENT_DOMAIN=settings.CURRENT_DOMAIN,
        MEDIA_URL=settings.MEDIA_URL,
        tasks=Task.objects.exclude(file=None).all()
    ))