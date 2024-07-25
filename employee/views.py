from django.shortcuts import render, redirect
from .models import *
from django.utils import timezone
from datetime import date


# Create your views here.
def addAttendanceEntry(request):
    todayEntries = AttendanceEntry.objects.filter(date=date.today(),employee=request.user).order_by('-loginTime')
    hasEntriesToday = True if len(todayEntries)>0 and todayEntries[0].logoffTime == None else False

    print(timezone.now())
    if request.method == 'POST':
        attendanceType = request.POST.get('attendance-type')

        if attendanceType == 'start':

            dailyAttendance_today = DailyAttendance.objects.filter(date=date.today(),employee=request.user)

            if len(dailyAttendance_today)==0:
                
                employeeTask = EmployeeTask.objects.filter(employee=request.user)[0]
                deviceType = request.POST.get('deviceType')
                deviceName = request.POST.get('deviceName')
                for task in employeeTask.task.all():
                    dailyTask = DailyTask(employee=request.user,task=task,date=date.today())
                    dailyTask.save()
                
                dailyAttendance = DailyAttendance(employee = request.user, isPresent = True, totalTasks=len(employeeTask.task.all()), deviceName=deviceName,deviceType=deviceType)
                dailyAttendance.save()

            else:
                dailyAttendance = dailyAttendance_today[0]

            attendanceEntry = AttendanceEntry(employee= request.user)
            attendanceEntry.save()

            dailyAttendance.attendanceEntries.add(attendanceEntry)
            dailyAttendance.save()

            return redirect('entry_tasks')

        elif attendanceType == 'break':
            dailyAttendance = DailyAttendance.objects.filter(date=date.today(),employee=request.user)[0]
            attendanceEntry = AttendanceEntry.objects.filter(date=date.today(),employee=request.user).order_by('-loginTime')[0]
            attendanceEntry.logoffTime = timezone.now()
            fromTime = attendanceEntry.loginTime
            toTime = attendanceEntry.logoffTime
            timediff = toTime - fromTime
            attendanceEntry.totalWorkingHours = timediff.total_seconds()/3600
            attendanceEntry.save()
            dailyAttendance.totalWorkingHours = dailyAttendance.totalWorkingHours + attendanceEntry.totalWorkingHours
            dailyAttendance.save()
            return redirect('logout')

        else:
            dailyAttendance = DailyAttendance.objects.filter(date=date.today(),employee=request.user)[0]
            attendanceEntry = AttendanceEntry.objects.filter(date=date.today(),employee=request.user).order_by('-loginTime')[0]
            attendanceEntry.logoffTime = timezone.now()
            dailyAttendance.exitTime = timezone.now()
            fromTime = attendanceEntry.loginTime
            toTime = attendanceEntry.logoffTime
            timediff = toTime - fromTime
            attendanceEntry.totalWorkingHours = timediff.total_seconds()/3600
            attendanceEntry.save()
            dailyAttendance.totalWorkingHours = dailyAttendance.totalWorkingHours + attendanceEntry.totalWorkingHours
        
            dailyAttendance.save()
            return redirect('logout')

    todayDate = timezone.now()
    totalTasksCount = 0
    totalCompletedTasksCount = 0
    if hasEntriesToday:
        dailyAttendance = DailyAttendance.objects.filter(date=date.today(),employee=request.user)[0]
        attendanceEntry = AttendanceEntry.objects.filter(date=date.today(),employee=request.user).order_by('-loginTime')[0]

        totalTasksCount = dailyAttendance.totalTasks
        totalCompletedTasksCount = dailyAttendance.completedCount
        
    return render(request,'attendance.html',{'hasEntriesToday':hasEntriesToday,'date':todayDate,'totalTasksCount':totalTasksCount,'totalCompletedTasksCount':totalCompletedTasksCount})


def getAllAttendanceEntries(request):
    dateVal = request.GET.get('date')
    if not dateVal:
        dateVal = date.today()
    dailyAttendances = DailyAttendance.objects.filter(date=dateVal).order_by('-date')
    return render(request,'all_attendance_entries.html',{'dailyAttendances':dailyAttendances})

def getDailyTasks(request):
    dailyTasks = DailyTask.objects.filter(employee=request.user,date=date.today())
    if request.method == 'POST':
        dailyAttendance = DailyAttendance.objects.filter(date=date.today(),employee=request.user)[0]
        
        count = dailyAttendance.completedCount
        for dailyTask in dailyTasks:
            hasCompleted = True if request.POST.get(str(dailyTask.pk),False)=='on' else False
            if hasCompleted:
                dailyTask.hasCompleted = True
                dailyTask.completedDateTime = timezone.now()
                dailyTask.save()
                dailyAttendance.completedTasks.add(dailyTask)
                count += 1

        dailyAttendance.completedCount = count
        dailyAttendance.save()
                
        return redirect('daily_tasks')

    return render(request,'daily_tasks.html',{'dailyTasks':dailyTasks})

def getAllEntryTasks(request):
    dailyTasks = DailyTask.objects.filter(employee=request.user,task__taskType='Entry',date=date.today())
    if request.method == 'POST':
        dailyAttendance = DailyAttendance.objects.filter(date=date.today(),employee=request.user)[0]
        
        count = dailyAttendance.completedCount
        for dailyTask in dailyTasks:
            hasCompleted = True if request.POST.get(str(dailyTask.pk),False)=='on' else False
            if hasCompleted:
                dailyTask.hasCompleted = True
                dailyTask.completedDateTime = timezone.now()
                dailyTask.save()
                dailyAttendance.completedTasks.add(dailyTask)
                count += 1

        dailyAttendance.completedCount = count
        dailyAttendance.save()
                
        return redirect('entry_tasks')

    return render(request,'daily_tasks.html',{'dailyTasks':dailyTasks})

def getAllExitTasks(request):
    dailyTasks = DailyTask.objects.filter(employee=request.user,task__taskType='Exit',date=date.today())
    if request.method == 'POST':
        dailyAttendance = DailyAttendance.objects.filter(date=date.today(),employee=request.user)[0]
        
        count = dailyAttendance.completedCount
        for dailyTask in dailyTasks:
            hasCompleted = True if request.POST.get(str(dailyTask.pk),False)=='on' else False
            if hasCompleted:
                dailyTask.hasCompleted = True
                dailyTask.completedDateTime = timezone.now()
                dailyTask.save()
                dailyAttendance.completedTasks.add(dailyTask)
                count += 1

        dailyAttendance.completedCount = count
        dailyAttendance.save()
                
        return redirect('exit_tasks')

    return render(request,'daily_tasks.html',{'dailyTasks':dailyTasks})

def applyLeave(request):
    if request.method == 'POST':
        deviceType = request.POST.get('deviceType')
        deviceName = request.POST.get('deviceName')
        leaveType = request.POST.get('leaveType')
        reason = request.POST.get('reason')
        dailyAttendance = DailyAttendance(employee = request.user, isPresent = False, deviceName=deviceName,deviceType=deviceType,leaveType=leaveType,reason=reason)
        dailyAttendance.save()
        return redirect('logout')

    todayDate = timezone.now()
    return render(request,'apply_leave.html',{'date':todayDate})

