from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView,LoginView
from teacher import views
urlpatterns = [
    path('',views.teacher_login,name="Teacher Login"),
    path('register',views.teacher_register,name="Teacher Register"),
    path('forgot-password/<str:user>',views.forgot_password,name="Teacher Forgot Password"),
    path('forgot-password-username',views.forgot_password_username,name="Teacher Forgot Password Username"),
    path('reset-password-forgot/<str:user>',views.reset_forgot_password,name="Reset Forgot Password"),
    
    path('afterloginTeacher',views.Teacher_After_Login,name="Teacher After Login"),

    path('profile',views.profile,name="Teacher Profile"),
    path('update-info',views.update_info,name="Teacher Update Info"),
    path('reset-password',views.reset_password,name="Teacher Reset Password"),

    path('view-student',views.view_student,name="View Student Record"),

    path('exam-page',views.exam_dashboard,name="Exam Page"),
    path('create-exam',views.create_exam,name="Create Exam Teacher"),
    path('upload-file/<str:id>',views.upload_file,name="Upload Excel"),
    path('create-exam-dashboard/<str:id>',views.create_exam_page,name="Create Exam Page"),
    
    path('insert-ques/<int:id>',views.insert_ques,name="Insert Ques Teacher"),

    path('update-ques/<int:id>/<int:eid>',views.update_ques,name="Update Ques"),
    path('delete-ques/<int:id>/<int:eid>',views.delete_ques,name="Delete Ques"),
    path('insert-ques-modify/<int:id>',views.insert_ques_modify_exam,name="Insert Question Modify Exam"),
    path('update-ques-modify/<int:id>/<int:eid>',views.update_ques_modify_exam,name="Update Question Modify Exam"),
    path('delete-ques-modify/<int:id>/<int:eid>',views.delete_ques_modify_exam,name="Delete Question Modify Exam"),

    path('modify-exam',views.modify_exam,name="Modify Exam"),
    path('modify-ques/<int:eid>',views.modify_ques,name="Modify Question"),
    path('modify-details/<int:eid>',views.modify_other_details,name="Modify Details"),
    path('modify-delete-exam/<int:eid>',views.delete_exam_modify_exam,name="Modify Exam Delete"),

    path('exam-after/<str:eid>',views.exam_after,name="Exam After"),
    path('modify-exam-after/<str:eid>',views.modify_exam_after,name="Modify Exam After"),
    path('insert-ques-modify-exam-after/<str:eid>',views.insert_ques_modify_exam_after,name="Insert Ques Modify Exam After"),
    path('modify-other-details-exam-after/<str:eid>',views.modify_other_details_exam_after,name="Modify Other Details Exam After"),
    path('update-ques-exam-after/<str:id>/<str:eid>',views.update_ques_after,name="Update Ques After"),
    path('delete-ques-exam-after/<str:id>/<str:eid>',views.delete_ques_exam_after,name="Delete Ques Exam After"),

    path('view-result-exam/<str:eid>',views.exam_result,name='Result Particular Exam'),

    path('remove-exam',views.remove_exam,name="Remove Exam"),
    path('delete-exam/<int:eid>',views.delete_exam,name="Delete Exam"),

    path('logout',views.Teacher_logout,name="Teacher Logout"),
]