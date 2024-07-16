from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

# Create your models here.
class adminTable(models.Model):  
    user = models.OneToOneField(User,on_delete=models.CASCADE)  
    #other fields here
    ForgotQuestion=(
        ('What was your first pet name?','What was your first pet name?'),
        ('Where were you born?','Where were you born?'),
        ('What is the first film you watched in a theatre?','What is the first film you watched in a theatre?'),
        ('What was your favourite subject in high school?','What was your favourite subject in high school?'),
        ('Where did you go on your favorite vacation as a child?','Where did you go on your favorite vacation as a child?'),
        )
    ques=models.CharField(max_length=400,choices=ForgotQuestion)
    ans=models.CharField(max_length=100)
    def __str__(self):  
          return  str(self.user)  

class ProgrammeTable(models.Model):
    ProgrammeName=models.CharField(max_length=30)

    def __str__(self):
        return self.ProgrammeName

class DepartmentTable(models.Model):
    DepartmentName=models.CharField(max_length=30)

    def __str__(self):
        return self.DepartmentName

class CourseTable(models.Model):
    CourseID=models.CharField(max_length=20)
    CourseName=models.CharField(max_length=100)

    def __str__(self):
        return self.CourseID

class UserTable(models.Model):
    status=(
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Rejected','Rejected'))
    role=(
        ('Teacher','Teacher'),
        ('Student','Student')
        )
    ForgotQuestion=(
        ('What was your first pet name?','What was your first pet name?'),
        ('Where were you born?','Where were you born?'),
        ('What is the first film you watched in a theatre?','What is the first film you watched in a theatre?'),
        ('What was your favourite subject in high school?','What was your favourite subject in high school?'),
        ('Where did you go on your favorite vacation as a child?','Where did you go on your favorite vacation as a child?'),
        )
    prefix=(
        ('Mr.','Mr.'),
        ('Mrs.','Mrs.'),
        ('Dr.','Dr.'),
        ('Ms.','Ms.'),
        ('Miss','Miss'),    
    )
    prefix=models.CharField(max_length=10,choices=prefix,blank=True)
    username=models.CharField(max_length=40,primary_key=True)
    password=models.CharField(max_length=300)
    role=models.CharField(max_length=40,choices=role)
    status=models.CharField(max_length=40,choices=status)
    name=models.CharField(max_length=40)
    email=models.CharField(max_length=40)
    mobile = models.CharField(max_length=20)
    programme=models.ForeignKey(ProgrammeTable,null=True,on_delete=models.CASCADE)
    department=models.ForeignKey(DepartmentTable,null=True,on_delete=models.CASCADE,blank=True)
    ques=models.CharField(max_length=400,choices=ForgotQuestion)
    ans=models.CharField(max_length=100)
    def __str__(self):
        return self.name
