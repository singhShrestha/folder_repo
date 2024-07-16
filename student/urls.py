from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView,LoginView
from student import views

urlpatterns = [
    path('',views.student_login,name="Student Login"),
    path('register',views.student_register,name="Student Register"),
    path('forgot-password/<str:user>',views.forgot_password,name="Student Forgot Password"),
    path('forgot-password-username',views.forgot_password_username,name="Student Forgot Password Username"),
    path('reset-password-forgot/<str:user>',views.reset_forgot_password,name="Student Reset Forgot Password"),

    path('afterloginStudent',views.Student_After_Login,name="Student After Login"),

    path('profile',views.profile,name="Student Profile"),
    path('update-info',views.update_info,name="Student Update Info"),
    path('reset-password',views.reset_password,name="Student Reset Password"),

    path('result-list',views.result_list,name="Result List"),
    path('exam-details/<str:id>',views.exam_details,name="Exam Details"),
    path('give-exam/<str:id>',views.give_exam,name="Give Exam"),
    path('attempted',views.attempted,name="Attempted"),
    path('attempted_list/<str:eid>',views.attempted_list,name="Attempted List"),

    path('logout',views.Student_logout,name="Student Logout"),
    # path('welcome',views.welcome_admin,name="Welcome Admin"),
    # path('logout/',views.logout_user,name="Logout User"),
]