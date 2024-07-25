from django.urls import path
from .views import *

urlpatterns = [
    path('add-attendance/',addAttendanceEntry,name='add_attendance'),
    path('all-attendance-entries/',getAllAttendanceEntries,name='all_attendance_entries'),
    path('daily-tasks/',getDailyTasks,name='daily_tasks'),
    path('entry-tasks/',getAllEntryTasks,name='entry_tasks'),
    path('exit-tasks/',getAllExitTasks,name='exit_tasks'),
    path('apply-leave/',applyLeave,name='apply_leave'),


]