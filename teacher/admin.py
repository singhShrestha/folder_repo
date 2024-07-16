from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Teacher)
admin.site.register(AssignmentTable)
admin.site.register(QuestionTable)
admin.site.register(PerformanceTable)
admin.site.register(ResultTable)
admin.site.register(OptionSelected)