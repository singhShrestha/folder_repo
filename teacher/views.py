from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from quiz.models import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.hashers import make_password
from student.models import *
from tablib import Dataset
from .resources import QuestionResource
from passlib.hash import pbkdf2_sha256

@login_required(login_url='Teacher Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Teacher_After_Login(request):
    current_user=request.user
    current_user_status=UserTable.objects.get(username=current_user).status
    
    if(current_user_status=='Pending'):
        return render(request,'teacher/waiting.html')
    elif(current_user_status=='Rejected'):
        u = User.objects.get(username = current_user)
        u.delete()
        UserTable.objects.get(username=current_user).delete()
        return render(request,'teacher/rejected.html')
    else:
        tInstance=Teacher.objects.get(user=request.user)
        ExamDetails=AssignmentTable.objects.filter(Tid=tInstance)
        Name=Teacher.objects.get(user=request.user).name
        Prefix=Teacher.objects.get(user=request.user).prefix
        context={'list':ExamDetails,'Name':Name,'Prefix':Prefix}
        return render(request,'teacher/teacher-dashboard.html',context)

@csrf_exempt
def teacher_register(request):
    if request.method=="POST":
        name=request.POST.get('tn')
        email=request.POST.get('em')
        department=request.POST.get('dept')
        departmentInstance=DepartmentTable.objects.get(DepartmentName=department)
        phone_number=request.POST.get('pn')
        user=request.POST.get('un')
        passw=request.POST.get('pass')
        prefix=request.POST.get('pre')
        ques=request.POST.get('forgot_pass_Q')
        ans=request.POST.get('forgot_pass_A')
        if User.objects.filter(username=user):
            messages.error(request,'Username is taken. Choose another.')
        else:
            user = User.objects.create_user(user, email, passw)
            user.save()
            enc_password=enc_password=pbkdf2_sha256.encrypt(passw)
            t=UserTable(prefix=prefix,username=user,password=enc_password,role='Teacher',status='Pending',name=name,email=email,department=departmentInstance,mobile=phone_number,ques=ques,ans=ans)
            t.save()
            return redirect('Teacher Login')
    
    departmentTable=DepartmentTable.objects.all()
    ques=['What was your first pet name?','Where were you born?','What is the first film you watched in a theatre?','What was your favourite subject in high school?','Where did you go on your favorite vacation as a child?']
    arr=['Mr.','Mrs.','Dr.','Ms.','Miss']
    return render(request,'teacher/teacher_register.html',{'list':departmentTable,'arr':arr,'ques':ques})

@csrf_exempt
def forgot_password(request,user):
    if request.method=='POST':
        ans=request.POST.get('ans')
        if(ans==UserTable.objects.get(username=user).ans):
            return redirect('Reset Forgot Password',user=user)
        else:
            messages.error(request,'Incorrect Answer.')
    ques=UserTable.objects.get(username=user).ques
    context={'name':user,'ques':ques}
    return render(request,'teacher/forgot_password.html',context)

@csrf_exempt
def forgot_password_username(request):
    if request.method=='POST':
        username=request.POST.get('username')
        if(UserTable.objects.filter(username=username,role='Teacher').exists()):
            return redirect('Teacher Forgot Password',user=username)
        else:
            messages.error(request,'Teacher with this username does not exist.')
    return render(request,'teacher/username.html')

@csrf_exempt
def reset_forgot_password(request,user):
    if request.method=='POST':
        newpass=request.POST.get('npass')
        enc_password=enc_password=pbkdf2_sha256.encrypt(newpass)
        UserTable.objects.filter(username=user).update(password=enc_password)
        Teacher.objects.filter(user=user).update(password=enc_password)
        newpassword=make_password(newpass)
        User.objects.filter(username=user).update(password=newpassword)
        return redirect('Teacher Login')
    context={'name':user}
    return render(request,'teacher/reset_password_forgot.html',context)

@csrf_exempt
def teacher_login(request):
    if request.method=="POST":
        user=request.POST.get('username')
        passw=request.POST.get('pass')
        userAuthenticate = authenticate(request,username=user,password=passw)
        if(User.objects.filter(username=user).exists()):
            uInstance=User.objects.get(username=user)
            present=UserTable.objects.filter(username=user,role='Teacher').exists()
            if present==False or userAuthenticate is None:
                messages.error(request,'Username or Password incorrect! Please enter Valid Credentials.')
            else:
                login(request,userAuthenticate)
                return redirect('Teacher After Login')
        else:
            messages.error(request,'Username or Password incorrect! Please enter Valid Credentials.')
    return render(request,'teacher/teacher_login.html')

@login_required(login_url='Teacher Login')
def Teacher_logout(request):
    logout(request)
    return redirect('Teacher Login')

@login_required(login_url='Teacher Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def profile(request):
    TeacherData=Teacher.objects.get(user=request.user)
    context={'list':TeacherData}
    return render(request,'teacher/profile.html',context)

@csrf_exempt
@login_required(login_url='Teacher Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update_info(request):
    if(request.method=="POST"):
        phone=request.POST.get('pn')
        username=request.POST.get('un')
        
        if(UserTable.objects.filter(username=username).exists() and username!=request.user.username ):
            messages.error(request,"Username already taken!")
        else:
            UserTable.objects.filter(username=request.user).update(username=username,mobile=phone)
            Teacher.objects.filter(user=request.user).update(user=username,mobile=phone)
            User.objects.filter(username=request.user).update(username=username)
            return redirect('Teacher Profile')

    TeacherData=Teacher.objects.get(user=request.user)
    context={'list':TeacherData}
    return render(request,'teacher/update_teacher.html',context)

@csrf_exempt
@login_required(login_url='Teacher Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reset_password(request):
    if(request.method=="POST"):
        currentpass=request.POST.get('cpass')
        newpass=request.POST.get('npass')
        passw=UserTable.objects.get(username=request.user.username).password
        result=pbkdf2_sha256.verify(currentpass,passw)
        if(result==False):
            messages.error(request,"Current Password is wrong!")
        else:
            enc_password=enc_password=pbkdf2_sha256.encrypt(newpass)
            UserTable.objects.filter(username=request.user).update(password=enc_password)
            Teacher.objects.filter(user=request.user).update(password=enc_password)
            newpassword=make_password(newpass)
            User.objects.filter(username=request.user).update(password=newpassword)
            return redirect('Teacher Update Info')

    return render(request,'teacher/reset_password.html')

@csrf_exempt
@login_required(login_url='Teacher Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def view_student(request):
    if request.method=="POST":
        pg=request.POST.get('pg')
        programmeList=ProgrammeTable.objects.all()
        pid=ProgrammeTable.objects.get(ProgrammeName=pg).id
        studentlist=Student.objects.filter(programme=pid)
        context={'list':studentlist,'programme':programmeList}
        return render(request,'teacher/student.html',context)

    programmeList=ProgrammeTable.objects.all()
    context={'programme':programmeList}
    return render(request,'teacher/student.html',context)

@login_required(login_url='Teacher Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def exam_dashboard(request):
    return render(request,'teacher/exam.html')

@csrf_exempt
@login_required(login_url='Teacher Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def create_exam(request):
    if request.method=="POST":
        ename=request.POST.get('examname')
        pg=request.POST.get('pg')
        cid=request.POST.get('cn')
        time=request.POST.get('time')
        inst=request.POST.get('message')
        #question_resource=QuestionResource()
        #dataset = Dataset()
        # new_ques = request.FILES['myfile']
        # imported_data = dataset.load(new_ques.read(),format='xlsx')
        # #print(imported_data)
        # for data in imported_data:
        # 	#print(data[1])
        # 	value = QuestionTable(
        # 		data[0],
        # 		data[1],
        # 		data[2],
        #         data[3],
        #         data[4],
        #         data[5],
        #         data[6],
        #         data[7],
        #         5
        # 		)
        # 	value.save()       
        
        cInstance=CourseTable.objects.get(CourseID=cid)

        programmeInstance=ProgrammeTable.objects.get(ProgrammeName=pg)
        id=Teacher.objects.get(user=request.user).smartID
        tInstance=Teacher.objects.get(smartID=id)
        
        e=AssignmentTable(ExamName=ename,ExamDuration=time,Programme=programmeInstance,Ccode=cInstance,Totalques=0,Tid=tInstance,Instruction=inst)
        
        e.save()
        ExamDetails=AssignmentTable.objects.get(ExamID=e.ExamID)
        context={'ExamDetails':ExamDetails}
        return render(request,'teacher/create_exam_dashboard.html',context)
    

    courselist=CourseTable.objects.all()
    programmelist=ProgrammeTable.objects.all()
    context={'courseList':courselist,'programmeList':programmelist}
    return render(request,'teacher/create_exam.html',context)

@login_required(login_url='Teacher Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def create_exam_page(request,id):
    eInstance=AssignmentTable.objects.get(ExamID=id)
    QuestionDetails=QuestionTable.objects.filter(TestID=eInstance)
    ExamDetails=AssignmentTable.objects.get(ExamID=id)
    
    context={'ExamDetails':ExamDetails,'list':QuestionDetails}
    return render(request,'teacher/create_exam_dashboard.html',context)

@csrf_exempt
@login_required(login_url='Teacher Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def insert_ques(request,id):
    if request.method=="POST":
        ques=request.POST.get('ques')
        op1=request.POST.get('op1')
        op2=request.POST.get('op2')
        op3=request.POST.get('op3')
        op4=request.POST.get('op4')
        ans=request.POST.get('answer')
        max_mark=request.POST.get('maxmarks')
        neg_mark=request.POST.get('negmarks')
        tInstance=AssignmentTable.objects.get(ExamID=id)
        
        q=QuestionTable(Ques=ques,Option1=op1,Option2=op2,option3=op3,option4=op4,ans=ans,max_mark=max_mark,neg_mark=neg_mark,TestID=tInstance)
        q.save()
        QuestionDetails=QuestionTable.objects.filter(TestID=id)
        ExamDetails=AssignmentTable.objects.get(ExamID=id)

        context={'ExamDetails':ExamDetails,'list':QuestionDetails}
        return render(request,'teacher/create_exam_dashboard.html',context)

    context={'ExamID':id}
    return render(request,'teacher/insert_ques.html',context)


@csrf_exempt
@login_required(login_url='Teacher Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update_ques(request,id,eid):
    if request.method=="POST":
        ques=request.POST.get('ques')
        option1=request.POST.get('op1')
        option2=request.POST.get('op2')
        option3=request.POST.get('op3')
        option4=request.POST.get('op4')
        ans=request.POST.get('answer')
        max_mark=request.POST.get('maxmarks')
        neg_mark=request.POST.get('negmarks')

        QuestionTable.objects.filter(QuesID=id).update(Ques=ques,Option1=option1,Option2=option2,option3=option3,option4=option4,ans=ans,max_mark=max_mark,neg_mark=neg_mark)
        return redirect('Create Exam Page', id=eid)
    
    QuestionData=QuestionTable.objects.get(QuesID=id)  
    context={'list':QuestionData,'ExamID':eid}  
    return render(request,'teacher/update_ques.html',context)

@login_required(login_url='Teacher Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_ques(request,id,eid):
    QuestionTable.objects.get(QuesID=id).delete()
    return redirect('Create Exam Page', id=eid)

@login_required(login_url='Teacher Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def modify_exam(request):
    tInstance=Teacher.objects.get(user=request.user)
    ExamDetails=AssignmentTable.objects.filter(Tid=tInstance)
    context={'list':ExamDetails}
    return render(request,'teacher/modify_exam.html',context)

@login_required(login_url='Teacher Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def modify_ques(request,eid):
    eInstance=AssignmentTable.objects.get(ExamID=eid)
    QuestionDetails=QuestionTable.objects.filter(TestID=eInstance)
    context={'list':QuestionDetails,'ExamID':eid}
    return render(request,'teacher/modify_ques.html',context)

@csrf_exempt
@login_required(login_url='Teacher Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def insert_ques_modify_exam(request,id):
    if request.method=="POST":
        ques=request.POST.get('ques')
        op1=request.POST.get('op1')
        op2=request.POST.get('op2')
        op3=request.POST.get('op3')
        op4=request.POST.get('op4')
        ans=request.POST.get('answer')
        max_mark=request.POST.get('maxmarks')
        neg_mark=request.POST.get('negmarks')
        tInstance=AssignmentTable.objects.get(ExamID=id)
        
        q=QuestionTable(Ques=ques,Option1=op1,Option2=op2,option3=op3,option4=op4,ans=ans,max_mark=max_mark,neg_mark=neg_mark,TestID=tInstance)
        q.save()
        QuestionDetails=QuestionTable.objects.filter(TestID=id)
        ExamDetails=AssignmentTable.objects.get(ExamID=id)

        context={'ExamDetails':ExamDetails,'list':QuestionDetails}
        return redirect('Modify Question',eid=id)
    
    context={'ExamID':id}
    return render(request,'teacher/insert_ques_modify.html',context)

@csrf_exempt
@login_required(login_url='Teacher Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update_ques_modify_exam(request,id,eid):
    if request.method=="POST":
        ques=request.POST.get('ques')
        option1=request.POST.get('op1')
        option2=request.POST.get('op2')
        option3=request.POST.get('op3')
        option4=request.POST.get('op4')
        ans=request.POST.get('answer')
        max_mark=request.POST.get('maxmarks')
        neg_mark=request.POST.get('negmarks')

        QuestionTable.objects.filter(QuesID=id).update(Ques=ques,Option1=option1,Option2=option2,option3=option3,option4=option4,ans=ans,max_mark=max_mark,neg_mark=neg_mark)
        return redirect('Modify Question',eid=eid)
    
    QuestionData=QuestionTable.objects.get(QuesID=id)  
    context={'list':QuestionData,'ExamID':eid}  
    return render(request,'teacher/update_ques_modify.html',context)

@login_required(login_url='Teacher Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_ques_modify_exam(request,id,eid):
    QuestionTable.objects.get(QuesID=id).delete()
    return redirect('Modify Question', eid=eid)

@csrf_exempt
@login_required(login_url='Teacher Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def modify_other_details(request,eid):
    if request.method=="POST":
        ename=request.POST.get('examname')
        pg=request.POST.get('pg')
        cid=request.POST.get('cn')
        time=request.POST.get('time')
        inst=request.POST.get('message')

        cInstance=CourseTable.objects.get(CourseID=cid)

        programmeInstance=ProgrammeTable.objects.get(ProgrammeName=pg)
        id=Teacher.objects.get(user=request.user).smartID
        tInstance=Teacher.objects.get(smartID=id)
        
        AssignmentTable.objects.filter(ExamID=eid).update(ExamName=ename,ExamDuration=time,Programme=programmeInstance,Ccode=cInstance,Totalques=0,Tid=tInstance,Instruction=inst)
        
        return redirect('Modify Exam')

    ExamDetails=AssignmentTable.objects.get(ExamID=eid)
    courselist=CourseTable.objects.all()
    programmelist=ProgrammeTable.objects.all()
    context={'courseList':courselist,'programmeList':programmelist,'ExamDetails':ExamDetails}
    return render(request,'teacher/modify_other_details.html',context)

@login_required(login_url='Teacher Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_exam_modify_exam(request,eid):
    tInstance=AssignmentTable.objects.get(ExamID=eid)
    QuestionTable.objects.filter(TestID=tInstance).delete()
    AssignmentTable.objects.get(ExamID=eid).delete()
    return redirect('Modify Exam')

@login_required(login_url='Teacher Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def remove_exam(request):
    tInstance=Teacher.objects.get(user=request.user)
    ExamDetails=AssignmentTable.objects.filter(Tid=tInstance)
    context={'list':ExamDetails}
    return render(request,'teacher/remove_exam.html',context)

@csrf_exempt
@login_required(login_url='Teacher Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_exam(request,eid):
    tInstance=AssignmentTable.objects.get(ExamID=eid)
    QuestionTable.objects.filter(TestID=tInstance).delete()
    AssignmentTable.objects.get(ExamID=eid).delete()
    return redirect('Remove Exam')

@login_required(login_url='Teacher Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def exam_after(request,eid):
    context={'ExamID':eid}
    return render(request,'teacher/exam_after.html',context)

@login_required(login_url='Teacher Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def modify_exam_after(request,eid):
    list=AssignmentTable.objects.get(ExamID=eid)
    QuestionList=QuestionTable.objects.filter(TestID=eid)
    context={'ExamDetails':list,'QuestionList':QuestionList}
    return render(request,'teacher/modify_exam_after.html',context)

@csrf_exempt
@login_required(login_url='Teacher Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def insert_ques_modify_exam_after(request,eid):
    if request.method=="POST":
        ques=request.POST.get('ques')
        op1=request.POST.get('op1')
        op2=request.POST.get('op2')
        op3=request.POST.get('op3')
        op4=request.POST.get('op4')
        ans=request.POST.get('answer')
        max_mark=request.POST.get('maxmarks')
        neg_mark=request.POST.get('negmarks')
        tInstance=AssignmentTable.objects.get(ExamID=eid)
        
        q=QuestionTable(Ques=ques,Option1=op1,Option2=op2,option3=op3,option4=op4,ans=ans,max_mark=max_mark,neg_mark=neg_mark,TestID=tInstance)
        q.save()
        QuestionDetails=QuestionTable.objects.filter(TestID=eid)
        ExamDetails=AssignmentTable.objects.get(ExamID=eid)

        context={'ExamDetails':ExamDetails,'QuestionList':QuestionDetails}
        return render(request,'teacher/modify_exam_after.html',context)

    context={'ExamID':eid}
    return render(request,'teacher/insert_ques_modify_exam_after.html',context)

@csrf_exempt
@login_required(login_url='Teacher Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def modify_other_details_exam_after(request,eid):
    if request.method=="POST":
        ename=request.POST.get('examname')
        pg=request.POST.get('pg')
        cid=request.POST.get('cn')
        time=request.POST.get('time')
        inst=request.POST.get('message')

        cInstance=CourseTable.objects.get(CourseID=cid)

        programmeInstance=ProgrammeTable.objects.get(ProgrammeName=pg)
        id=Teacher.objects.get(user=request.user).smartID
        tInstance=Teacher.objects.get(smartID=id)
        
        AssignmentTable.objects.filter(ExamID=eid).update(ExamName=ename,ExamDuration=time,Programme=programmeInstance,Ccode=cInstance,Totalques=0,Tid=tInstance,Instruction=inst)
        
        return redirect('Modify Exam After',eid=eid)

    ExamDetails=AssignmentTable.objects.get(ExamID=eid)
    courselist=CourseTable.objects.all()
    programmelist=ProgrammeTable.objects.all()
    context={'courseList':courselist,'programmeList':programmelist,'ExamDetails':ExamDetails}
    return render(request,'teacher/modify_other_details_exam_after.html',context)

@csrf_exempt
@login_required(login_url='Teacher Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update_ques_after(request,id,eid):
    if request.method=="POST":
        ques=request.POST.get('ques')
        option1=request.POST.get('op1')
        option2=request.POST.get('op2')
        option3=request.POST.get('op3')
        option4=request.POST.get('op4')
        ans=request.POST.get('answer')
        max_mark=request.POST.get('maxmarks')
        neg_mark=request.POST.get('negmarks')

        QuestionTable.objects.filter(QuesID=id).update(Ques=ques,Option1=option1,Option2=option2,option3=option3,option4=option4,ans=ans,max_mark=max_mark,neg_mark=neg_mark)
        return redirect('Modify Exam After',eid=eid)
    
    QuestionData=QuestionTable.objects.get(QuesID=id)  
    context={'list':QuestionData,'ExamID':eid}  
    return render(request,'teacher/update_ques_after.html',context)

@login_required(login_url='Teacher Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_ques_exam_after(request,id,eid):
    QuestionTable.objects.get(QuesID=id).delete()
    return redirect('Modify Exam After', eid=eid)

@login_required(login_url='Teacher Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def exam_result(request,eid):
    List=ResultTable.objects.filter(TestId=eid)
    context={'list':List,'ExamID':eid}
    return render(request,'teacher/view_result.html',context)

@csrf_exempt
@login_required(login_url='Teacher Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def upload_file(request,id):
    if request.method == 'POST':
        question_resource=QuestionResource()
        dataset = Dataset()
        new_ques = request.FILES['myfile']
        if not new_ques.name.endswith('xlsx'):
            messages.error(request,'Wrong Format! File should be .xlsx')
            context={'ExamID':id}
            return render(request,'teacher/upload_file.html',context)

        imported_data = dataset.load(new_ques.read(),format='xlsx')
        f=0
        for data in imported_data:
            if(len(data)!=8):
                f=1
        
        if(f==1):
            messages.error(request,'Excel file does not contain 8 columns.')
            context={'ExamID':id}
            return render(request,'teacher/upload_file.html',context)
        
        f=0
        for data in imported_data:
            print(data[0]==None)
            if(data[0]==None):
                f=1
        
        if(f==1):
            messages.error(request,'Wrong Format! Column 1 should not have empty entry.')
            context={'ExamID':id}
            return render(request,'teacher/upload_file.html',context)

        f=0
        for data in imported_data:
            if(data[1]==None):
                f=1
        
        if(f==1):
            messages.error(request,'Wrong Format! Column 2 should not have empty entry.')
            context={'ExamID':id}
            return render(request,'teacher/upload_file.html',context)

        f=0
        for data in imported_data:
            if(data[2]==None):
                f=1
        
        if(f==1):
            messages.error(request,'Wrong Format! Column 3 should not have empty entry.')
            context={'ExamID':id}
            return render(request,'teacher/upload_file.html',context)
        
        f=0
        for data in imported_data:
            if(data[3]==None):
                f=1
        
        if(f==1):
            messages.error(request,'Wrong Format! Column 4 should not have empty entry.')
            context={'ExamID':id}
            return render(request,'teacher/upload_file.html',context)

        f=0
        for data in imported_data:
            if(data[4]==None):
                f=1
        
        if(f==1):
            messages.error(request,'Wrong Format! Column 5 should not have empty entry.')
            context={'ExamID':id}
            return render(request,'teacher/upload_file.html',context)

        f=0
        for data in imported_data:
            if(data[5]!='Option 1' and data[5]!='Option 2' and data[5] != 'Option 3' and data[5]!='Option 4'):
                f=1
        
        if(f==1):
            messages.error(request,'Wrong Format! Column 6 should contain answers in the format of Option 1 or Option 2 or Option 3 or Option 4.')
            context={'ExamID':id}
            return render(request,'teacher/upload_file.html',context)
        
        f=0
        for data in imported_data:
            if(type(data[6])!=int):
                if(type(data[6])!=float):
                    if(data[6].isdecimal()==False):
                        f=1
        
        if(f==1):
            messages.error(request,'Wrong Format! Column 7 should contain decimal value.')
            context={'ExamID':id}
            return render(request,'teacher/upload_file.html',context)
        
        f=0
        for data in imported_data:
            if(type(data[7])!=int):
                if(type(data[7])!=float):
                    if(data[7].isdecimal()==False):
                        f=1
        
        if(f==1):
            messages.error(request,'Wrong Format! Column 8 should contain decimal value.')
            context={'ExamID':id}
            return render(request,'teacher/upload_file.html',context)

        tInstance=AssignmentTable.objects.get(ExamID=id)
        print(imported_data)
        for data in imported_data:
            value = QuestionTable(Ques=data[0],Option1=data[1],Option2=data[2],option3=data[3],option4=data[4],ans=data[5],max_mark=float(data[6]),neg_mark=float(data[7]),TestID=tInstance)
            value.save()        
        
        return redirect('Create Exam Page',id=id)
    context={'ExamID':id}
    return render(request,'teacher/upload_file.html',context)
