from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Task)
admin.site.register(DailyTask)
admin.site.register(AttendanceEntry)
admin.site.register(DailyAttendance)
admin.site.register(EmployeeTask)