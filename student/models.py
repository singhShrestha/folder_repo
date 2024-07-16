from django.db import models
from quiz.models import *
from teacher.models import *

class Student(models.Model):
    user=models.CharField(max_length=40)
    password=models.CharField(max_length=300)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    mobile = models.CharField(max_length=20)
    programme=models.ForeignKey(ProgrammeTable,null=True,on_delete=models.CASCADE)
    smartID=models.AutoField(primary_key=True)
    
    def __str__(self):
        return str(self.smartID)