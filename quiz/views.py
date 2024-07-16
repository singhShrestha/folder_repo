from django.shortcuts import render,redirect,reverse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.views.decorators.cache import cache_control
from student.models import *
from teacher.models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from passlib.hash import pbkdf2_sha256

def home_view(response):
    return render(response,'index.html')

@login_required(login_url='Admin login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def student(request):
    pending_count=UserTable.objects.filter(status='Pending',role='Student').count()
    context={'total_pending':pending_count}
    return render(request,'admin/student.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def teacher(request):
    pending_count=UserTable.objects.filter(status='Pending',role='Teacher').count()
    context={'total_pending':pending_count}
    return render(request,'admin/teacher.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def exam(request):
    return render(request,'admin/exam.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def student_record(request,id):
    pid=ProgrammeTable.objects.get(ProgrammeName=id).id
    StudentList=Student.objects.filter(programme=pid)
    return render(request,'admin/student_record.html',{'list': StudentList})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def teacher_record(request,id):
    did=DepartmentTable.objects.get(DepartmentName=id).id
    TeacherList=Teacher.objects.filter(department=did)
    return render(request,'admin/teacher_record.html',{'list': TeacherList})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def exam_courses_list(request,id):
    cid=CourseTable.objects.get(CourseName=id).id
    AssignmentList=AssignmentTable.objects.filter(Ccode=cid)
    
    i=0
    count=[0]*AssignmentList.count()
    while(i<AssignmentList.count()):
        numberOfQuestions=QuestionTable.objects.filter(TestID=AssignmentList[i])
        for j in numberOfQuestions:
            count[i]=count[i]+j.max_mark
        
        i=i+1
    
    l=zip(AssignmentList,count)
    context={'l':l}

    return render(request,'admin/exam_under_course.html',context)

@csrf_exempt
def admin_login(request):
    if request.method=="POST":
        user=request.POST.get('username')
        passw=request.POST.get('pass')
        if(User.objects.filter(username=user).exists()):
            uInstance=User.objects.get(username=user)
            user = authenticate(request,username=user,password=passw)
            present=adminTable.objects.filter(user=uInstance).exists()
            if present==False or user is None:
                messages.error(request,'Username or Password incorrect! Please enter Valid Credentials.')
            else:
                login(request,user)
                return redirect('Welcome Admin')
        else:
            messages.error(request,'Username or Password incorrect! Please enter Valid Credentials.')
    
    return render(request,'admin/admin_login.html',context={})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def logout_user(request):
    logout(request)
    return redirect('Logout User')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def welcome_admin(request):
    total_students=Student.objects.all().count()
    total_teachers=Teacher.objects.all().count()
    total_courses=CourseTable.objects.all().count()
    total_department=DepartmentTable.objects.all().count()
    total_programme=ProgrammeTable.objects.all().count()
    total_exam=AssignmentTable.objects.all().count()
    
    context={'total_student':total_students,'total_teacher':total_teachers,'total_courses':total_courses,'total_department':total_department,'total_programme':total_programme,'total_exam':total_exam}
    return render(request,'admin/admin_dashboard.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def student_pending(request):
    StudentList=UserTable.objects.filter(status='Pending',role='Student')
    return render(request,'admin/student_pending_list.html',{'list':StudentList})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def student_approved(request,id):
    data=UserTable.objects.get(username=id)
    data.status='Approved'
    data.save()
    s=Student(user=id,password=data.password,name=data.name,email=data.email,programme=data.programme,mobile=data.mobile)
    s.save()
    return redirect('Admin Student Pending')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def teacher_pending(request):
    TeacherList=UserTable.objects.filter(status='Pending',role='Teacher')
    return render(request,'admin/teacher_pending_list.html',{'list':TeacherList})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def teacher_approved(request,id):
    data=UserTable.objects.get(username=id)
    data.status='Approved'
    data.save()
    t=Teacher(prefix=data.prefix,user=id,password=data.password,name=data.name,email=data.email,department=data.department,mobile=data.mobile)
    t.save()
    return redirect('Admin Teacher Pending')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def teacher_rejected(request,id):
    uInstance=User.obejcts.get(user=id)
    data=UserTable.objects.get(user=uInstance)
    data.status='Rejected'
    data.save()
    return redirect('Admin Teacher Pending')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def student_rejected(request,id):
    data=UserTable.objects.get(username=id)
    data.status='Rejected'
    data.save()
    return redirect('Admin Student Pending')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def teacher_delete(request,id):
    department=Teacher.objects.get(user=id).department
    UserTable.objects.get(username=id).delete()
    Teacher.objects.get(user=id).delete()
    User.objects.get(username=id).delete()
    return redirect('Teacher Record',id=department)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def student_delete(request,id):
    programme=Student.objects.get(user=id).programme
    UserTable.objects.get(username=id).delete()
    Student.objects.get(user=id).delete()
    User.objects.get(username=id).delete()
    return redirect('Student Record',id=programme)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def department(request):
    departmentList=DepartmentTable.objects.all()
    context={'list':departmentList}
    return render(request,'admin/department_record.html',context)

@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def department_update(request,id):
    if request.method=="POST":
        name=request.POST.get('dn')
        present=DepartmentTable.objects.filter(DepartmentName=name).exists()
        if(present==True and name!=id):
            messages.error(request,'Department Already Exists!')
        else:
            DepartmentTable.objects.filter(DepartmentName=id).update(DepartmentName=name)
            return redirect('Department')

    DepartmentList=DepartmentTable.objects.get(DepartmentName=id)
    context={'list':DepartmentList}
    return render(request,'admin/update_department.html',context)

@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def insert_department(request):
    if request.method=="POST":
        name=request.POST.get('dn')
        present=DepartmentTable.objects.filter(DepartmentName=name).exists()
        if(present==True):
            messages.error(request,'Department Already Exists!')
        else:
            d=DepartmentTable(DepartmentName=name)
            d.save()
            return redirect('Department')

    return render(request,'admin/insert_department.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def department_delete(request,id):
    UserTableList=User.objects.all()
    did=DepartmentTable.objects.get(DepartmentName=id)
    list=Teacher.objects.filter(department=did)
    for i in list:
        for j in UserTableList:
            if i.user==j.username:
                User.objects.get(username=i.user).delete()
    DepartmentTable.objects.get(DepartmentName=id).delete()
    return redirect('Department')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def course(request):
    CourseList=CourseTable.objects.all()
    context={'list':CourseList}
    return render(request,'admin/course_record.html',context)

@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def course_update(request,id):
    if request.method=="POST":
        cid=request.POST.get('cid')
        name=request.POST.get('cn')
        present=CourseTable.objects.filter(CourseID=cid).exists()
        if(present==True and cid!=id):
            messages.error(request,'Course Already Exists!')
        else:
            CourseTable.objects.filter(CourseID=id).update(CourseID=cid,CourseName=name)
            return redirect('Course')

    CourseList=CourseTable.objects.get(CourseID=id)
    context={'list':CourseList}
    return render(request,'admin/update_course.html',context)

@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def insert_course(request):
    if request.method=="POST":
        cid=request.POST.get('cid')
        name=request.POST.get('cn')
        present=CourseTable.objects.filter(CourseID=cid).exists()
        if(present==True):
            messages.error(request,'Course Already Exists!')
        else:
            c=CourseTable(CourseID=cid,CourseName=name)
            c.save()
            return redirect('Course')

    return render(request,'admin/insert_course.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def course_delete(request,id):
    CourseTable.objects.get(CourseID=id).delete()
    return redirect('Course')

@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def student_update(request,id):
    if request.method=="POST":
        name=request.POST.get('sn')
        email=request.POST.get('em')
        programme=request.POST.get('pg')
        phone=request.POST.get('pn')
        pid=ProgrammeTable.objects.get(ProgrammeName=programme)
        Student.objects.filter(user=id).update(name=name,email=email,mobile=phone,programme=pid)
        UserTable.objects.filter(username=id).update(name=name,email=email,mobile=phone,programme=pid)
        return redirect('Student Record',id=programme)
    
    ProgrammeList=ProgrammeTable.objects.all()
    StudentData=Student.objects.get(user=id)
    context={'list':StudentData,'programmeList':ProgrammeList}
    return render(request,'admin/student_update.html',context)

@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def teacher_update(request,id):
    if request.method=="POST":
        name=request.POST.get('tn')
        email=request.POST.get('em')
        department=request.POST.get('dept')
        phone=request.POST.get('pn')
        did=DepartmentTable.objects.get(DepartmentName=department)
        Teacher.objects.filter(user=id).update(name=name,email=email,mobile=phone,department=did)
        UserTable.objects.filter(username=id).update(name=name,email=email,mobile=phone,department=did)
        return redirect('Teacher Record',id=department)

    DepartmentList=DepartmentTable.objects.all()
    TeacherData=Teacher.objects.get(user=id)
    context={'list':TeacherData,'departmentList':DepartmentList}
    return render(request,'admin/teacher_update.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def total_programme(request):
    programmeList=ProgrammeTable.objects.all()
    i=0
    count=[0]*programmeList.count()
    while(i<programmeList.count()):
        count[i]=Student.objects.filter(programme=programmeList[i]).count()
        i=i+1
    
    l=zip(programmeList,count)
    context={'l':l}
    return render(request,'admin/total_student_programme.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def total_courses(request):
    courseList=CourseTable.objects.all()
    i=0
    count=[0]*courseList.count()
    while(i<courseList.count()):
        count[i]=AssignmentTable.objects.filter(Ccode=courseList[i]).count()
        i=i+1
    
    l=zip(courseList,count)
    context={'l':l}
    return render(request,'admin/exam_courses.html',context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def total_department(request):
    departmentList=DepartmentTable.objects.all()

    i=0
    count=[0]*departmentList.count()
    while(i<departmentList.count()):
        count[i]=Teacher.objects.filter(department=departmentList[i]).count()
        i=i+1
    
    l=zip(departmentList,count)
    context={'l':l}

    return render(request,'admin/total_teacher_department.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def programme(request):
    programmeList=ProgrammeTable.objects.all()
    context={'list':programmeList}
    return render(request,'admin/programme_record.html',context)

@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def programme_update(request,id):
    if request.method=="POST":
        name=request.POST.get('pn')
        present=ProgrammeTable.objects.filter(ProgrammeName=name).exists()
        if(present==True and name!=id):
            messages.error(request,'Programme Already Exists!')
        else:
            ProgrammeTable.objects.filter(ProgrammeName=id).update(ProgrammeName=name)
            return redirect('Programme')

    ProgrammeList=ProgrammeTable.objects.get(ProgrammeName=id)
    context={'list':ProgrammeList}
    return render(request,'admin/update_programme.html',context)

@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def insert_programme(request):
    if request.method=="POST":
        name=request.POST.get('pn')
        present=ProgrammeTable.objects.filter(ProgrammeName=name).exists()
        if(present==True):
            messages.error(request,'Programme Already Exists!')
        else:
            p=ProgrammeTable(ProgrammeName=name)
            p.save()
            return redirect('Programme')

    return render(request,'admin/insert_programme.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def programme_delete(request,id):
    ProgrammeTable.objects.get(ProgrammeName=id).delete()
    return redirect('Programme')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='Admin login')
def exam_result(request,id):
    list=ResultTable.objects.filter(TestId=id)
    ccode=AssignmentTable.objects.get(ExamID=id).Ccode
    Cname=CourseTable.objects.get(CourseID=ccode).CourseName
    context={'CourseName':Cname,'list':list}
    return render(request,'admin/view_result.html',context)

@csrf_exempt
def forgot_password(request,user):
    if request.method=='POST':
        ans=request.POST.get('ans')
        uInstance=User.objects.get(username=user)
        if(ans==adminTable.objects.get(user=uInstance).ans):
            return redirect('Admin Reset Forgot Password',user=user)
        else:
            messages.error(request,'Incorrect Answer.')
    uInstance=User.objects.get(username=user)
    ques=adminTable.objects.get(user=uInstance).ques
    context={'name':user,'ques':ques}
    return render(request,'admin/forgot_password.html',context)

@csrf_exempt
def forgot_password_username(request):
    if request.method=='POST':
        username=request.POST.get('username')
        if(User.objects.filter(username=username).exists()):
            uInstance=User.objects.get(username=username)
            if(adminTable.objects.filter(user=uInstance).exists()):
                return redirect('Admin Forgot Password',user=username)
            else:
                messages.error(request,'Admin with this username does not exist.')
        else:
            messages.error(request,'Admin with this username does not exist.')
        
    return render(request,'admin/username.html')

@csrf_exempt
def reset_forgot_password(request,user):
    if request.method=='POST':
        newpass=request.POST.get('npass')
        enc_password=enc_password=pbkdf2_sha256.encrypt(newpass)
        uInstance=User.objects.get(username=user)
        newpassword=make_password(newpass)
        User.objects.filter(username=user).update(password=newpassword)
        return redirect('Admin login')
    context={'name':user}
    return render(request,'admin/reset_password_forgot.html',context)