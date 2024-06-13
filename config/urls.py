from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from courses.views import index, login, register, logout

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index, name='index'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),

    path('courses/', include('courses.urls'), name='visitka')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
