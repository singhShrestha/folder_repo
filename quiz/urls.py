from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView,LoginView
from quiz import views

urlpatterns = [
    path('',views.admin_login,name="Admin login"),
    path('welcome',views.welcome_admin,name="Welcome Admin"),
    path('logout/',views.logout_user,name="Logout User"),
    path('student',views.student,name="Student"),
    path('teacher',views.teacher,name="Teacher"),
    path('exam',views.exam,name="Exam"),
    
    path('forgot-password/<str:user>',views.forgot_password,name="Admin Forgot Password"),
    path('forgot-password-username',views.forgot_password_username,name="Admin Forgot Password Username"),
    path('reset-password-forgot/<str:user>',views.reset_forgot_password,name="Admin Reset Forgot Password"),
    
    path('total-programme',views.total_programme,name="Total Programmes"),
    path('total-department',views.total_department,name="Total Departments"),
    path('total-courses',views.total_courses,name='Total Courses'),

    path('department-record',views.department,name="Department"),
    path('department-insert',views.insert_department,name="Insert Department"),
    path('department-update/<str:id>',views.department_update,name="Update Department"),
    path('department-delete/<str:id>',views.department_delete,name="Delete Department"),

    path('course-record',views.course,name="Course"),
    path('course-update/<str:id>',views.course_update,name="Update Course"),
    path('course-delete/<str:id>',views.course_delete,name="Delete Course"),
    path('course-insert',views.insert_course,name="Insert Course"),
    
    path('programme-record',views.programme,name="Programme"),
    path('programme-update/<str:id>',views.programme_update,name="Update Programme"),
    path('programme-delete/<str:id>',views.programme_delete,name="Delete Programme"),
    path('programme-insert',views.insert_programme,name="Insert Programme"),

    path('student-update/<str:id>',views.student_update,name='Update Student'),
    path('teacher-update/<str:id>',views.teacher_update,name='Update Teacher'),

    path('student-record/<str:id>',views.student_record,name="Student Record"),
    path('teacher-record/<str:id>',views.teacher_record,name="Teacher Record"),
    path('exam-courses-list/<str:id>',views.exam_courses_list,name="Exam Courses List"),

    path('student-pending',views.student_pending,name="Admin Student Pending"),
    path('student-approved/<str:id>',views.student_approved,name="Student Approved"),
    path('student-rejected/<str:id>',views.student_rejected,name="Student Rejected"),
    path('teacher-pending',views.teacher_pending,name="Admin Teacher Pending"),
    path('teacher-approved/<str:id>',views.teacher_approved,name="Teacher Approved"),
    path('teacher-rejected/<str:id>',views.teacher_rejected,name="Teacher Rejected"),

    path('deleteTeacher/<str:id>',views.teacher_delete,name="Delete Teacher"),
    path('deleteStudent/<str:id>',views.student_delete,name="Delete Student"),

    path('exam-result/<int:id>',views.exam_result,name="Exam Result"),
]