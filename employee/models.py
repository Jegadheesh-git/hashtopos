from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    name = models.CharField(max_length=50)
    taskType = models.CharField(max_length=50,choices=(('Entry','Entry'),('Exit','Exit')))
    def __str__(self) -> str:
        return self.name

class EmployeeTask(models.Model):
    employee = models.ForeignKey(User,on_delete=models.CASCADE)
    task = models.ManyToManyField(Task)

    def __str__(self) -> str:
        return str(self.employee)

class DailyTask(models.Model):
    employee = models.ForeignKey(User,on_delete=models.CASCADE)
    task = models.ForeignKey(Task,on_delete=models.CASCADE)
    date = models.DateField()
    completedDateTime = models.DateTimeField(null=True,blank=True)
    hasCompleted = models.BooleanField(default=False)   

class AttendanceEntry(models.Model):
    date = models.DateField(auto_now_add=True)
    employee = models.ForeignKey(User,on_delete=models.CASCADE)
    loginTime = models.DateTimeField(auto_now_add=True)
    logoffTime = models.DateTimeField(null=True,blank=True)
    totalWorkingHours = models.FloatField(null=True,blank=True)

    def __str__(self) -> str:
        return str(self.employee) + ' - '+str(self.date)+' from : '+str(self.loginTime)+' to : '+str(self.logoffTime)

class DailyAttendance(models.Model):
    date = models.DateField(auto_now_add=True)
    employee = models.ForeignKey(User,on_delete=models.CASCADE)
    isPresent = models.BooleanField(default=False)
    entryTime = models.DateTimeField(auto_now_add=True)
    exitTime = models.DateTimeField(null=True,blank=True)
    leaveType = models.CharField(max_length=50,choices=(('Casual Leave','Casual Leave'),('Medical Leave','Medical Leave'),('Religious Leave','Religious Leave'),('Other','Other')),null=True,blank=True)
    reason = models.CharField(max_length=250,null=True,blank=True)
    completedTasks = models.ManyToManyField(DailyTask)
    totalTasks = models.IntegerField(default=0)
    completedCount = models.IntegerField(default=0)

    deviceType = models.CharField(max_length=50)
    deviceName = models.CharField(max_length=250,null=True,blank=True)

    attendanceEntries = models.ManyToManyField(AttendanceEntry)
    totalWorkingHours = models.FloatField(default=0)

class Salary(models.Model):
    employee = models.ForeignKey(User,on_delete=models.CASCADE)
    baseSalary = models.FloatField()
    rentalAllowance = models.FloatField()
    travelAllowance = models.FloatField()
    foodAllowance = models.FloatField()
    otherAllowance = models.FloatField()
    totalNetSalary = models.FloatField()

class MonthlySalary(models.Model):
    employee = models.ForeignKey(User,on_delete=models.CASCADE)
    creditedOn = models.DateTimeField(auto_now_add=True)
    paymentMode = models.CharField(max_length=50, choices=(('Cash','Cash'),('UPI','UPI'),('Bank Transfer','Bank Transfer')))
    totalWorkingHours = models.FloatField()
    totalWorkedHours = models.FloatField()
    salaryAmount = models.FloatField()
    bonusAmount = models.FloatField()
    totalAmount = models.FloatField()
    paymentInfo = models.CharField(max_length=250)
    reasonForBonus = models.CharField(max_length=250,null=True,blank=True)
    totalWorkingDays = models.IntegerField()
    totalPresentDays = models.IntegerField()
    totalLeaveDays = models.IntegerField()