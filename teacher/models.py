from django.db import models
from quiz.models import *
from django.utils import timezone
from student.models import *

class Teacher(models.Model):
    prefix=(
        ('Mr.','Mr.'),
        ('Mrs.','Mrs.'),
        ('Dr.','Dr.'),
        ('Ms.','Ms.'),
        ('Miss','Miss'),    
    )
    prefix=models.CharField(max_length=10,choices=prefix)
    user=models.CharField(max_length=40)
    password=models.CharField(max_length=300)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    mobile = models.CharField(max_length=20)
    department=models.ForeignKey(DepartmentTable,null=True,on_delete=models.CASCADE)
    smartID=models.AutoField(primary_key=True)
    
    def __str__(self):
        return str(self.smartID)

class AssignmentTable(models.Model):
    ExamID=models.AutoField(primary_key=True)
    ExamName=models.CharField(max_length=150)
    ExamDuration=models.DecimalField(max_digits=500,decimal_places=2)
    Programme=models.ForeignKey(ProgrammeTable,on_delete=models.CASCADE,null=True)
    Ccode=models.ForeignKey(CourseTable,on_delete=models.CASCADE,null=True)
    Totalques=models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    Tid=models.ForeignKey(Teacher,on_delete=models.CASCADE,null=True)
    Instruction=models.CharField(max_length=700,null=True,blank=True)

    def __str__(self):
        return str(self.ExamID)
    
class QuestionTable(models.Model):
    QuesID=models.AutoField(primary_key=True)
    Ques=models.CharField(max_length=2000)
    Option1=models.CharField(max_length=1000)
    Option2=models.CharField(max_length=1000)
    option3=models.CharField(max_length=1000)
    option4=models.CharField(max_length=1000)
    ANS_CHOICES = (
    ("Option 1", "Option 1"),
    ("Option 2", "Option 2"),
    ("Option 3", "Option 3"),
    ("Option 4", "Option 4")
    )
    ans=models.CharField(max_length=1000,choices=ANS_CHOICES)
    max_mark=models.DecimalField(max_digits=50,decimal_places=2)
    neg_mark=models.DecimalField(max_digits=10,decimal_places=2)
    TestID=models.ForeignKey(AssignmentTable,on_delete=models.CASCADE,null=True)

    def __self__(self):
        return str(self.QuesID)

class PerformanceTable(models.Model):
    SId=models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
    TestID=models.ForeignKey(AssignmentTable,on_delete=models.CASCADE,null=True)
    QId=models.ForeignKey(QuestionTable,on_delete=models.CASCADE,null=True)
    Max_mark=models.DecimalField(max_digits=500,decimal_places=2)
    Mark_Obtained=models.DecimalField(max_digits=500,decimal_places=2)

    def __str__(self):
        return str(self.id)

class ResultTable(models.Model):
    SId=models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
    TestId=models.ForeignKey(AssignmentTable,on_delete=models.CASCADE,null=True)
    Max_Total_Mark=models.DecimalField(max_digits=500,decimal_places=2)
    TotalMarkObtained=models.DecimalField(max_digits=500,decimal_places=2)
    date_attempted=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

class OptionSelected(models.Model):
    TestId=models.ForeignKey(AssignmentTable,null=True,on_delete=models.CASCADE)
    QuestionId=models.ForeignKey(QuestionTable,null=True,on_delete=models.CASCADE)
    SId=models.ForeignKey(Student,null=True,on_delete=models.CASCADE)
    ans_selected=models.CharField(max_length=10)

    def __str__(self):
        return str(self.TestId)