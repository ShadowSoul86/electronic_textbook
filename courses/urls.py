from django.urls import path
from .views import courses_list, course_item

urlpatterns = [
    path('', courses_list, name='courses_list'),
    path('item/<int:course_id>/', course_item, name='course_item'),
    path('item/<int:course_id>/<int:task_id>/', course_item, name='course_item'),
]
