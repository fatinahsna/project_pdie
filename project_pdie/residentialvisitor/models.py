from django.db import models

# Create your models here.
class Resident(models.Model):
    resID = models.CharField(max_length=10, primary_key=True)
    resName = models.TextField(max_length=255)
    resIC = models.CharField(max_length=14)
    resGender = models.TextField(max_length=6)
    resRace = models.TextField(max_length=20)
    resPhoneno = models.CharField(max_length=20)
    houseNo = models.CharField(max_length=6)
    street = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    resPassword = models.CharField(max_length=10)

class Guard(models.Model):
    guardID = models.CharField(max_length=5, primary_key=True)
    guardName = models.TextField(max_length=255)
    guardPhoneno = models.CharField(max_length=20)
    guardPost = models.CharField(max_length=6, default="Post 1")
    guardShift = models.CharField(max_length=15, default="Day Shift")
    guardPassword = models.CharField(max_length=10)

class Admin(models.Model):
    adminID = models.CharField(max_length=10, primary_key=True)
    adminName = models.TextField(max_length=255)
    adminIC = models.CharField(max_length=14)
    adminPhoneno = models.CharField(max_length=20)
    adminPassword = models.CharField(max_length=10)

class Visitor(models.Model):
    visName = models.TextField(max_length=255)
    visIC = models.CharField(max_length=14)
    visPhoneno = models.CharField(max_length=20)
    plateNo = models.CharField(max_length=20)
    houseNo = models.CharField(max_length=6)
    street = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    purpose = models.TextField(max_length=255)
    date = models.DateField()
    timeIn = models.TimeField(null=True)
    timeOut = models.TimeField(null=True)
    duration = models.CharField(max_length=5) #days example : 1 day, 3 days, 7 days
    status = models.TextField(max_length=10, default='Registered') #Registered / Check in / Check out
    resID = models.ForeignKey(Resident, on_delete=models.CASCADE, null=True)
    guardID = models.ForeignKey(Guard, on_delete=models.CASCADE, null=True)

class Event(models.Model):
    eventName = models.TextField(max_length=255)
    houseNo = models.CharField(max_length=6)
    street = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    duration = models.CharField(max_length=5) #days example : 1 day, 3 days, 7 days
    numOfVisitor = models.IntegerField()
    message = models.TextField(max_length=255, null=True)
    resID = models.ForeignKey(Resident, on_delete=models.CASCADE, null=True)

class ReportIssue(models.Model):
    issueName = models.TextField(max_length=255)
    description = models.TextField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    status = models.TextField(max_length=10, default='Submitted') #Submitted / In progress / Completed
    measuresTaken = models.TextField(max_length=255, null=True)
    resID = models.ForeignKey(Resident, on_delete=models.CASCADE, null=True)
    guardID = models.ForeignKey(Guard, on_delete=models.CASCADE, null=True)
    adminID = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True)

class ReportGuard(models.Model):
    guardName = models.TextField(max_length=255)
    description = models.TextField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    status = models.TextField(max_length=10, default='Submitted') #Submitted / In progress / Completed
    measuresTaken = models.TextField(max_length=255, null=True)
    resID = models.ForeignKey(Resident, on_delete=models.CASCADE, null=True)
    guardID = models.ForeignKey(Guard, on_delete=models.CASCADE, null=True)
    adminID = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True)
