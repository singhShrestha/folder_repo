from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(adminTable)
admin.site.register(UserTable)
admin.site.register(ProgrammeTable)
admin.site.register(DepartmentTable)
admin.site.register(CourseTable)