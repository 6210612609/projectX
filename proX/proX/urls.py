"""proX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users.views import main, students, tutors
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',include("users.urls")),
    path('about/', main.about, name = 'about'),
    path('admin/', admin.site.urls),
    path('users/register/',main.register, name='register'),
    path('users/student_register/',students.student_register.as_view(), name='student_register'),
    path('users/tutor_register/',tutors.tutor_register.as_view(), name='tutor_register'),
    path('users/login/',main.login_request, name='login'),
    path('users/logout/',main.logout_view, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
