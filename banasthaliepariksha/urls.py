"""banasthaliepariksha URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,include
from django.contrib.auth.views import LogoutView,LoginView
from quiz import views as v1
from teacher import views as v2
from student import views as v3

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',v1.home_view,name="Main Page"),
    path('admin-head/',include('quiz.urls')),
    path('teacher/',include('teacher.urls')),
    path('student/',include('student.urls')),
    # path('adminlogin', LoginView.as_view(template_name='admin/admin_login.html'),name='adminlogin'),
    # path('afterlogin',views.afterloginaction,name="afterlogin"),
]