from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Student
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from quiz.models import *
from django.contrib.auth.hashers import make_password
from teacher.models import *
from passlib.hash import pbkdf2_sha256

@login_required(login_url='Student Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Student_After_Login(request):
    current_user=request.user
    current_user_status=UserTable.objects.get(username=current_user).status
    if(current_user_status=='Pending'):
        return render(request,'student/waiting.html')
    elif(current_user_status=='Rejected'):
        u = User.objects.get(username = current_user)
        u.delete()
        UserTable.objects.get(username=current_user).delete()
        return render(request,'student/rejected.html')
    else:
        pname=Student.objects.get(user=request.user).programme
        pid=ProgrammeTable.objects.get(ProgrammeName=pname).id
        StudentID=Student.objects.get(user=request.user).smartID
        
        List = AssignmentTable.objects.filter(Programme=pid)
        
        for i in List:
            if(ResultTable.objects.filter(SId=StudentID,TestId=i.ExamID).exists()):
                List=List.exclude(ExamID=i.ExamID)
        
        for j in List:
            QuestionList=QuestionTable.objects.filter(TestID=j.ExamID).count()
            if(QuestionList==0):
                List=List.exclude(ExamID=j.ExamID)

        Name=Student.objects.get(user=request.user).name
        context={'list':List,'Name':Name}
        return render(request,'student/student-dashboard.html',context)

@csrf_exempt
def student_register(request):
    if request.method=="POST":
        name=request.POST.get('sn')
        email=request.POST.get('em')
        programme=request.POST.get('pg')
        programmeInstance=ProgrammeTable.objects.get(ProgrammeName=programme)
        phone_number=request.POST.get('pn')
        user=request.POST.get('un')
        passw=request.POST.get('pass')
        ques=request.POST.get('forgot_pass_Q')
        ans=request.POST.get('forgot_pass_A')
        if User.objects.filter(username=user):
            messages.error(request,'Username is taken. Choose another.')
        else:
            user = User.objects.create_user(user, email, passw)
            user.save()
            enc_password=enc_password=pbkdf2_sha256.encrypt(passw)
            s=UserTable(username=user,password=enc_password,role='Student',status='Pending',name=name,email=email,programme=programmeInstance,mobile=phone_number,ques=ques,ans=ans)
            s.save()
            return redirect('Student Login')
    
    programmeTable=ProgrammeTable.objects.all()
    ques=['What was your first pet name?','Where were you born?','What is the first film you watched in a theatre?','What was your favourite subject in high school?','Where did you go on your favorite vacation as a child?']

    return render(request,'student/student_register.html',{'list':programmeTable,'ques':ques})

@csrf_exempt
def student_login(request):
    if request.method=="POST":
        user=request.POST.get('username')
        passw=request.POST.get('pass')
        
        userAuthenticate = authenticate(request,username=user,password=passw)
        if(User.objects.filter(username=user).exists()):
            uInstance=User.objects.get(username=user)
            present=UserTable.objects.filter(username=user,role='Student').exists()
            if present==False or userAuthenticate is None:
                messages.error(request,'Username or Password incorrect! Please enter Valid Credentials.')
            else:
                login(request,userAuthenticate)
                return redirect('Student After Login')
        else:
            messages.error(request,'Username or Password incorrect! Please enter Valid Credentials.')
        
    return render(request,'student/student_login.html')

@login_required(login_url='Student Login')
def Student_logout(request):
    logout(request)
    return redirect('Student Login')

@login_required(login_url='Student Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def profile(request):
    StudentData=Student.objects.get(user=request.user)
    context={'list':StudentData}
    return render(request,'student/profile.html',context)

@csrf_exempt
@login_required(login_url='Student Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update_info(request):
    if(request.method=="POST"):
        phone=request.POST.get('pn')
        username=request.POST.get('un')
        if(UserTable.objects.filter(username=username).exists() and username!=request.user.username ):
            messages.error(request,"Username already taken!")
        else:
            UserTable.objects.filter(username=request.user).update(username=username,mobile=phone)
            Student.objects.filter(user=request.user).update(user=username,mobile=phone)
            User.objects.filter(username=request.user).update(username=username)
            return redirect('Student Profile')

    StudentData=Student.objects.get(user=request.user)
    context={'list':StudentData}
    return render(request,'student/update_student.html',context)

@csrf_exempt
def forgot_password(request,user):
    if request.method=='POST':
        ans=request.POST.get('ans')
        if(ans==UserTable.objects.get(username=user).ans):
            return redirect('Student Reset Forgot Password',user=user)
        else:
            messages.error(request,'Incorrect Answer.')
    ques=UserTable.objects.get(username=user).ques
    context={'name':user,'ques':ques}
    return render(request,'student/forgot_password.html',context)

@csrf_exempt
def forgot_password_username(request):
    if request.method=='POST':
        username=request.POST.get('username')
        if(UserTable.objects.filter(username=username,role='Student').exists()):
            return redirect('Student Forgot Password',user=username)
        else:
            messages.error(request,'Student with this username does not exist.')
    return render(request,'student/username.html')

@csrf_exempt
def reset_forgot_password(request,user):
    if request.method=='POST':
        newpass=request.POST.get('npass')
        enc_password=enc_password=pbkdf2_sha256.encrypt(newpass)
        UserTable.objects.filter(username=user).update(password=enc_password)
        Student.objects.filter(user=user).update(password=enc_password)
        newpassword=make_password(newpass)
        User.objects.filter(username=user).update(password=newpassword)
        return redirect('Student Login')
    context={'name':user}
    return render(request,'student/reset_password_forgot.html',context)

@csrf_exempt
@login_required(login_url='Student Login')
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
            Student.objects.filter(user=request.user).update(password=enc_password)
            newpassword=make_password(newpass)
            User.objects.filter(username=request.user).update(password=newpassword)
            return redirect('Student Update Info')

    return render(request,'student/reset_password.html')

@login_required(login_url='Student Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def result_list(request):
    sid=Student.objects.get(user=request.user).smartID
    list=ResultTable.objects.filter(SId=sid)
    context={'list':list}
    return render(request,'student/result.html',context)

@csrf_exempt
@login_required(login_url='Student Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def give_exam(request,id):
    if request.method=="POST":
        QuestionList=QuestionTable.objects.filter(TestID=id)
        j=0
        sInstance=Student.objects.get(user=request.user)
        tInstance=AssignmentTable.objects.get(ExamID=id)
        a=[0]*QuestionList.count()

        QuestionList=QuestionTable.objects.filter(TestID=id)
        p=0
        d=[0]*QuestionList.count()
        f=0
        for y in QuestionList:
            d[p]=y.QuesID
            p=p+1
        for i in d:
            for key in request.POST:
                print(key,i,int(key)==i)
                if(int(key)==i):
                    value = request.POST[key]
                    f=1
            if(f!=1):
                value=0
            f=0
            a[j]=value
            j=j+1
        
        j=0
        for s in QuestionList:
            qInstance=QuestionTable.objects.get(QuesID=s.QuesID)
            o=OptionSelected(TestId=tInstance,QuestionId=qInstance,SId=sInstance,ans_selected=a[j])
            o.save()
            j=j+1
        
        j=0
        for i in QuestionList:
            qInstance=QuestionTable.objects.get(QuesID=i.QuesID)
            print(i.ans,a[j],i.ans==a[j])
            if(i.ans==a[j]):
                p=PerformanceTable(SId=sInstance,TestID=tInstance,QId=qInstance,Max_mark=i.max_mark,Mark_Obtained=i.max_mark)
                p.save()
            elif(a[j]==0):
                p=PerformanceTable(SId=sInstance,TestID=tInstance,QId=qInstance,Max_mark=i.max_mark,Mark_Obtained=0)
                p.save()
            else:
                p=PerformanceTable(SId=sInstance,TestID=tInstance,QId=qInstance,Max_mark=i.max_mark,Mark_Obtained=-i.neg_mark)
                p.save()
            
            j=j+1
        sid=Student.objects.get(user=request.user).smartID
        PerformanceList=PerformanceTable.objects.filter(TestID=id,SId=sid)
        Total_Mark_Maximum=0
        Total_Mark=0
        for i in PerformanceList:
            Total_Mark_Maximum=Total_Mark_Maximum+i.Max_mark
            Total_Mark=Total_Mark+i.Mark_Obtained
        
        r=ResultTable(SId=sInstance,TestId=tInstance,Max_Total_Mark=Total_Mark_Maximum,TotalMarkObtained=Total_Mark)
        
        r.save()
        context={'Total_Mark_Obtained':Total_Mark,'Total_Mark_Maximum':Total_Mark_Maximum}
        return render(request,'student/after_exam.html',context)
    
    ExamDetails=AssignmentTable.objects.get(ExamID=id)
    QuestionList=QuestionTable.objects.filter(TestID=id)
    count=0
    for i in QuestionList:
        count=count+i.max_mark
    
    context={'list':QuestionList,'ExamDetails':ExamDetails,'MaximumMarks':count}
    return render(request,'student/ques.html',context)

@login_required(login_url='Student Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def exam_details(request,id):
    QuestionList=QuestionTable.objects.filter(TestID=id)
    count=0
    for i in QuestionList:
        count=count+i.max_mark
    
    ExamDetails=AssignmentTable.objects.get(ExamID=id)
    context={'ExamDetails':ExamDetails,'MaximumMarks':count}
    return render(request,'student/exam_details.html',context)

@csrf_exempt
@login_required(login_url='Student Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def attempted(request):
    pname=Student.objects.get(user=request.user).programme
    pid=ProgrammeTable.objects.get(ProgrammeName=pname).id
    StudentID=Student.objects.get(user=request.user).smartID
    
    List = AssignmentTable.objects.filter(Programme=pid)
    ResultList=ResultTable.objects.filter(SId=StudentID)
    for i in List:
        if(ResultTable.objects.filter(SId=StudentID,TestId=i.ExamID).exists()==False):
            List=List.exclude(ExamID=i.ExamID)
            ResultList=ResultList.exclude(TestId=i.ExamID)
    
    print('List',List)
    l=zip(List,ResultList)
    context={'l':l}
    return render(request,'student/attempted.html',context)

@csrf_exempt
@login_required(login_url='Student Login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def attempted_list(request,eid):
    sid=Student.objects.get(user=request.user).smartID
    QuestionList=QuestionTable.objects.filter(TestID=eid)
    studentId=Student.objects.get(user=request.user).smartID
    PerformanceList=PerformanceTable.objects.filter(TestID=eid,SId=sid)
    OptionList=OptionSelected.objects.filter(TestId=eid,SId=studentId)
    l=zip(QuestionList,PerformanceList,OptionList)
    context={'l':l}
    print(OptionList)
    return render(request,'student/attempted_list.html',context)