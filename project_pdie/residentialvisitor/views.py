from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from residentialvisitor.models import Resident,Guard,Admin,Visitor,Event,ReportIssue,ReportGuard
from django.db.models import Q, Count
import requests
import datetime

# Create your views here.
#==========================================RESIDENT=============================================================
# Resident/Admin login__________________________________________________________________________________________
def resident_loginpage(request):
    return render(request, 'resident_login.html')

def resident_login(request):
    if (request.method == 'GET'):
        return render(request, 'resident_login.html', {'message':' '})
    else:
        resID = request.POST['resID']
        resPassword = request.POST['resPassword']
        myresident = Resident.objects.all().filter(resID=resID, resPassword=resPassword)
        for x in myresident:
            if x.resID==resID and x.resPassword==resPassword:
                url = reverse('resident_dashboard', kwargs={'resID':resID})
                return HttpResponseRedirect(url)
        return render(request, 'resident_login.html', {'message':'Your password is incorrect.'})

# Resident dashboard____________________________________________________________________________________________
def resident_dashboard(request, resID):
    myresident = Resident.objects.get(resID=resID)
    dict = {
        'myresident':myresident,
    }
    return render(request, 'resident_dashboard.html', dict)

# Resident registration_________________________________________________________________________________________
def resident_registration(request, resID):
    myresident = Resident.objects.get(resID=resID)
    myvisitor = Visitor.objects.filter(resID=resID).order_by('-date').values()
    myevent = Event.objects.filter(resID=resID).order_by('-date').values()
    dict = {
        'myresident':myresident,
        'myvisitor':myvisitor,
        'myevent':myevent
    }
    return render(request, 'resident_registration.html', dict)

# Resident register new visitor_________________________________________________________________________________
def register_visitor(request, resID):
    if request.method == "GET":
        myresident = Resident.objects.get(resID=resID)
        dict = {
            'myresident':myresident,
        }
        return render(request, 'residentregister_visitor.html', dict)
    else:
        v_visName = request.POST['visName']
        v_visIC = request.POST['visIC']
        v_visPhoneno = request.POST['visPhoneno']
        v_plateNo = request.POST['plateNo']
        v_houseNo = request.POST['houseNo']
        v_street = request.POST['street']
        v_purpose = request.POST['purpose']
        v_date = request.POST['date']
        v_duration = request.POST['duration']
        v_address = v_houseNo + ", Jalan Kesuma " + v_street + ", Bandar Tasik Kesuma, 43700, Beranang, Selangor"
        myresident = Resident.objects.get(resID=resID)
        newvisitor = Visitor(visName=v_visName, visIC=v_visIC, visPhoneno=v_visPhoneno, plateNo=v_plateNo, houseNo=v_houseNo, street=v_street, address=v_address, purpose=v_purpose, date=v_date, duration=v_duration, resID=myresident)
        newvisitor.save()
        url = reverse('resident_qrcode', kwargs={'resID':resID})
        return HttpResponseRedirect(url)
    
# Resident register new event__________________________________________________________________________________
def register_event(request, resID):
    if request.method == "GET":
        myresident = Resident.objects.get(resID=resID)
        dict = {
            'myresident':myresident,
        }
        return render(request, 'residentregister_event.html', dict)
    else:
        e_eventName = request.POST['eventName']
        e_houseNo = request.POST['houseNo']
        e_street = request.POST['street']
        e_date = request.POST['date']
        e_time = request.POST['time']
        e_duration = request.POST['duration']
        e_numberOfVisitor = request.POST['numOfVisitor']
        e_message = request.POST['message']
        e_address = e_houseNo + ", Jalan Kesuma " + e_street + ", Bandar Tasik Kesuma, 43700, Beranang, Selangor"
        myresident = Resident.objects.get(resID=resID)
        newevent = Event(eventName=e_eventName,houseNo=e_houseNo,street=e_street,address=e_address,date=e_date,time=e_time,duration=e_duration,numOfVisitor=e_numberOfVisitor,message=e_message,resID=myresident)
        newevent.save()
        url = reverse('resident_qrcode', kwargs={'resID':resID})
        return HttpResponseRedirect(url)

# Resident update/edit event____________________________________________________________________________________
def update_event(request, resID, id):
    if request.method == "GET":
        myresident = Resident.objects.get(resID=resID)
        myevent = Event.objects.get(id=id)
        dict = {
            'myresident':myresident,
            'myevent':myevent,
        }
        return render(request, 'residentupdate_event.html', dict)
    else:
        myevent = Event.objects.get(id=id)
        e_eventName = request.POST['eventName']
        e_houseNo = request.POST['houseNo']
        e_street = request.POST['street']
        e_date = request.POST['date']
        e_time = request.POST['time']
        e_duration = request.POST['duration']
        e_numberOfVisitor = request.POST['numOfVisitor']
        e_message = request.POST['message']
        if (e_eventName != ''):
            myevent.eventName = e_eventName
        if (e_houseNo != ''):
            myevent.houseNo = e_houseNo
        if (e_street != ''):
            myevent.street = e_street
            myevent.address = e_houseNo + ", Jalan Kesuma " + e_street + ", Bandar Tasik Kesuma, 43700, Beranang, Selangor"
        if (e_date != ''):
            myevent.date = e_date
        if (e_time != ''):
            myevent.time = e_time
        if (e_duration != ''):
            myevent.duration = e_duration
        if (e_numberOfVisitor != ''):
            myevent.numOfVisitor = e_numberOfVisitor
        if (e_message != ''):
            myevent.message = e_message
        myevent.save()
        url = reverse('resident_registration', kwargs={'resID':resID})
        return HttpResponseRedirect(url)
    
# Resident delete event________________________________________________________________________________________
def delete_event(request, resID, id):
    if request.method == "POST":
        myresident = Resident.objects.get(resID=resID)
        myevent = Event.objects.get(id=id)
        myevent.delete()
        url = reverse('resident_registration', kwargs={'resID':resID})
        return HttpResponseRedirect(url)

# Resident get QR code__________________________________________________________________________________________
def resident_qrcode(request, resID):
    myresident = Resident.objects.get(resID=resID)
    dict = {
        'myresident':myresident,
    }
    return render(request, 'resident_qrcode.html', dict)

# Resident report_______________________________________________________________________________________________
def resident_report(request, resID):
    myresident = Resident.objects.get(resID=resID)
    myissue = ReportIssue.objects.filter(resID=resID).order_by('-date').values()
    myreportguard = ReportGuard.objects.filter(resID=resID).order_by('-date').values()
    dict = {
        'myresident':myresident,
        'myissue':myissue,
        'myreportguard':myreportguard
    }
    return render(request, 'resident_report.html', dict)

# Resident report new issue_____________________________________________________________________________________
def report_issue(request, resID):
    if request.method == "GET":
        myresident = Resident.objects.get(resID=resID)
        dict = {
            'myresident':myresident,
        }
        return render(request, 'residentreport_issue.html', dict)
    else:
        i_issueName = request.POST['issueName']
        i_description = request.POST['description']
        i_date = request.POST['date']
        i_time = request.POST['time']
        myresident = Resident.objects.get(resID=resID)
        newissue = ReportIssue(issueName=i_issueName,description=i_description,date=i_date,time=i_time,status='Submitted',resID=myresident)
        newissue.save()
        url = reverse('resident_report', kwargs={'resID':resID})
        return HttpResponseRedirect(url)
    
# Resident update reported issue________________________________________________________________________________
def update_issue(request, resID, id):
    if request.method == "GET":
        myresident = Resident.objects.get(resID=resID)
        myissue = ReportIssue.objects.get(id=id)
        dict = {
            'myresident':myresident,
            'myissue':myissue
        }
        return render(request, 'residentupdate_issue.html', dict)
    else:
        myissue = ReportIssue.objects.get(id=id)
        i_issueName = request.POST['issueName']
        i_description = request.POST['description']
        i_date = request.POST['date']
        i_time = request.POST['time']
        if (i_issueName != ''):
            myissue.issueName = i_issueName
        if (i_description != ''):
            myissue.description = i_description
        if (i_date != ''):
            myissue.date = i_date
        if (i_time != ''):
            myissue.time = i_time
        myissue.save()
        url = reverse('resident_report', kwargs={'resID':resID})
        return HttpResponseRedirect(url)
    
# Resident delete reported issue________________________________________________________________________________
def delete_issue(request, resID, id):
    if request.method == "POST":
        myissue = ReportIssue.objects.get(id=id)
        if (myissue.status == 'Submitted'):
            myissue.delete()
        url = reverse('resident_report', kwargs={'resID':resID})
        return HttpResponseRedirect(url)
    
# Resident report guard_________________________________________________________________________________________
def report_guard(request, resID):
    if request.method == "GET":
        myresident = Resident.objects.get(resID=resID)
        dict = {
            'myresident':myresident,
        }
        return render(request, 'residentreport_guard.html', dict)
    else:
        g_guardName = request.POST['guardName']
        data = Guard.objects.get(guardName=g_guardName)
        a = data.guardID
        i_description = request.POST['description']
        i_date = request.POST['date']
        i_time = request.POST['time']
        myresident = Resident.objects.get(resID=resID)
        myguard = Guard.objects.get(guardID=a)
        newreportguard = ReportGuard(guardName=g_guardName,description=i_description,date=i_date,time=i_time,status='Submitted',resID=myresident, guardID=myguard)
        newreportguard.save()
        url = reverse('resident_report', kwargs={'resID':resID})
        return HttpResponseRedirect(url)
    
# Resident update reported guard________________________________________________________________________________
def update_guard(request, resID, id):
    if request.method == "GET":
        myresident = Resident.objects.get(resID=resID)
        myreportguard = ReportGuard.objects.get(id=id)
        dict = {
            'myresident':myresident,
            'myreportguard':myreportguard
        }
        return render(request, 'residentupdate_guard.html', dict)
    else:
        myreportguard = ReportGuard.objects.get(id=id)
        i_description = request.POST['description']
        i_date = request.POST['date']
        i_time = request.POST['time']
        if (i_description != ''):
            myreportguard.description = i_description
        if (i_date != ''):
            myreportguard.date = i_date
        if (i_time != ''):
            myreportguard.time = i_time
        myreportguard.save()
        url = reverse('resident_report', kwargs={'resID':resID})
        return HttpResponseRedirect(url)
    
# Resident delete reported guard________________________________________________________________________________
def delete_guard(request, resID, id):
    if request.method == "POST":
        myreportguard = ReportGuard.objects.get(id=id)
        if (myreportguard.status == 'Submitted'):
            myreportguard.delete()
        url = reverse('resident_report', kwargs={'resID':resID})
        return HttpResponseRedirect(url)

# Resident guard________________________________________________________________________________________________
def resident_guard(request, resID):
    myresident = Resident.objects.get(resID=resID)
    dict = {
        'myresident':myresident,
    }
    return render(request, 'resident_guard.html', dict)



#==========================================GUARD================================================================
# Guard login___________________________________________________________________________________________________
def guard_loginpage(request):
    return render(request, 'guard_login.html')

def guard_login(request):
    if (request.method == 'GET'):
        return render(request, 'guard_login.html', {'message':' '})
    else:
        guardID = request.POST['guardID']
        guardPassword = request.POST['guardPassword']
        myguard = Guard.objects.all().filter(guardID=guardID, guardPassword=guardPassword)
        myadmin = Admin.objects.all().filter(adminID=guardID, adminPassword=guardPassword)
        for x in myguard:
            if x.guardID==guardID and x.guardPassword==guardPassword:
                url = reverse('guard_dashboard', kwargs={'guardID':guardID})
                return HttpResponseRedirect(url)
        for y in myadmin:
                if y.adminID==guardID and y.adminPassword==guardPassword:
                    url = reverse('admin_dashboard', kwargs={'adminID':guardID})
                    return HttpResponseRedirect(url)
        return render(request, 'guard_login.html', {'message':'Your password is incorrect.'})

# Guard dashboard_______________________________________________________________________________________________
def guard_dashboard(request, guardID):
    myguard = Guard.objects.get(guardID=guardID)
    dict = {
        'myguard':myguard,
    }
    return render(request, 'guard_dashboard.html', dict)

# Guard visitor_________________________________________________________________________________________________
def guard_visitor(request, guardID):
    myguard = Guard.objects.get(guardID=guardID)
    myvisitor = Visitor.objects.all().order_by('-date').values()
    dict = {
        'myguard':myguard,
        'myvisitor':myvisitor
    }
    return render(request, 'guard_visitor.html', dict)

# Guard visitor filtered________________________________________________________________________________________
def guardfilter_visitor(request, guardID):
    myguard = Guard.objects.get(guardID=guardID)
    query = Q()
    visName = request.GET.get('visName', '')
    plateNo = request.GET.get('plateNo', '')
    houseNo = request.GET.get('houseNo', '')
    street = request.GET.get('street', '')
    date = request.GET.get('date', '')
    if visName:
        query &= Q(visName__icontains=visName)
    if plateNo:
        query &= Q(plateNo__icontains=plateNo)
    if houseNo:
        query &= Q(houseNo__icontains=houseNo)
    if street:
        query &= Q(street__icontains=street)
    if date:
        query &= Q(date__icontains=date)
    myvisitor = Visitor.objects.filter(query)
    dict = {
        'myguard':myguard,
        'myvisitor':myvisitor
    }
    return render(request, 'guard_visitor.html', dict)


# Guard register new visitor____________________________________________________________________________________
def guardregister_visitor(request, guardID):
    if request.method == "GET":
        myguard = Guard.objects.get(guardID=guardID)
        dict = {
            'myguard':myguard,
        }
        return render(request, 'guardregister_visitor.html', dict)
    else:
        v_visName = request.POST['visName']
        v_visIC = request.POST['visIC']
        v_visPhoneno = request.POST['visPhoneno']
        v_plateNo = request.POST['plateNo']
        v_houseNo = request.POST['houseNo']
        v_street = request.POST['street']
        v_purpose = request.POST['purpose']
        v_date = request.POST['date']
        v_duration = request.POST['duration']
        v_address = v_houseNo + ", Jalan Kesuma " + v_street + ", Bandar Tasik Kesuma, 43700, Beranang, Selangor"
        myguard = Guard.objects.get(guardID=guardID)
        newvisitor = Visitor(visName=v_visName, visIC=v_visIC, visPhoneno=v_visPhoneno, plateNo=v_plateNo, houseNo=v_houseNo, street=v_street, address=v_address, purpose=v_purpose, date=v_date, duration=v_duration, guardID=myguard)
        newvisitor.save()
        url = reverse('guard_visitor', kwargs={'guardID':guardID})
        return HttpResponseRedirect(url)
    
# Guard visitor details_________________________________________________________________________________________
def guarddetails_visitor(request, guardID, id):
    myguard = Guard.objects.get(guardID=guardID)
    myvisitor = Visitor.objects.get(id=id)
    dict = {
        'myguard':myguard,
        'myvisitor':myvisitor
    }
    return render(request, 'guarddetails_visitor.html', dict)

# Guard check-in visitor________________________________________________________________________________________
def guardcheckin_visitor(request, guardID, id):
    myguard = Guard.objects.get(guardID=guardID)
    myvisitor = Visitor.objects.get(id=id)
    myvisitor.timeIn = datetime.datetime.now().time()
    myvisitor.status = "Checked-In"
    myvisitor.save()
    url = reverse('guard_visitor', kwargs={'guardID':guardID})
    return HttpResponseRedirect(url)

# Guard check-out visitor________________________________________________________________________________________
def guardcheckout_visitor(request, guardID, id):
    myguard = Guard.objects.get(guardID=guardID)
    myvisitor = Visitor.objects.get(id=id)
    myvisitor.timeOut = datetime.datetime.now().time()
    myvisitor.status = "Checked-Out"
    myvisitor.save()
    url = reverse('guard_visitor', kwargs={'guardID':guardID})
    return HttpResponseRedirect(url)
    
# Guard event___________________________________________________________________________________________________
def guard_event(request, guardID):
    myguard = Guard.objects.get(guardID=guardID)
    myevent = Event.objects.all().order_by('-date').values()
    dict = {
        'myguard':myguard,
        'myevent':myevent,
    }
    return render(request, 'guard_event.html', dict)

# Guard report__________________________________________________________________________________________________
def guard_report(request, guardID):
    myguard = Guard.objects.get(guardID=guardID)
    myissue = ReportIssue.objects.all().order_by('-date').values()
    dict = {
        'myguard':myguard,
        'myissue':myissue
    }
    return render(request, 'guard_report.html', dict)

# Guard report new issue________________________________________________________________________________________
def guardreport_issue(request, guardID):
    if request.method == "GET":
        myguard = Guard.objects.get(guardID=guardID)
        dict = {
            'myguard':myguard,
        }
        return render(request, 'guardreport_issue.html', dict)
    else:
        i_issueName = request.POST['issueName']
        i_description = request.POST['description']
        i_date = request.POST['date']
        i_time = request.POST['time']
        myguard = Guard.objects.get(guardID=guardID)
        newissue = ReportIssue(issueName=i_issueName,description=i_description,date=i_date,time=i_time,status='Submitted',guardID=myguard)
        newissue.save()
        url = reverse('guard_report', kwargs={'guardID':guardID})
        return HttpResponseRedirect(url)

# Guard update reported issue____________________________________________________________________________________
def guardupdate_issue(request, guardID, id):
    if request.method == "GET":
        myguard = Guard.objects.get(guardID=guardID)
        myissue = ReportIssue.objects.get(id=id)
        dict = {
            'myguard':myguard,
            'myissue':myissue
        }
        return render(request, 'guardupdate_issue.html', dict)
    else:
        myissue = ReportIssue.objects.get(id=id)
        i_issueName = request.POST['issueName']
        i_description = request.POST['description']
        i_date = request.POST['date']
        i_time = request.POST['time']
        if (i_issueName != ''):
            myissue.issueName = i_issueName
        if (i_description != ''):
            myissue.description = i_description
        if (i_date != ''):
            myissue.date = i_date
        if (i_time != ''):
            myissue.time = i_time
        myissue.save()
        url = reverse('guard_report', kwargs={'guardID':guardID})
        return HttpResponseRedirect(url)
    
# Guard delete reported issue________________________________________________________________________________
def guarddelete_issue(request, guardID, id):
    if request.method == "POST":
        myissue = ReportIssue.objects.get(id=id)
        if (myissue.status == 'Submitted'):
            myissue.delete()
        url = reverse('guard_report', kwargs={'guardID':guardID})
        return HttpResponseRedirect(url)


#==========================================ADMIN================================================================
# Admin dashboard____________________________________________________________________________________________
def admin_dashboard(request, adminID):
    myadmin = Admin.objects.get(adminID=adminID)
    dict = {
        'myadmin':myadmin,
    }
    return render(request, 'admin_dashboard.html', dict)

# Admin resident______________________________________________________________________________________________
def admin_resident(request, adminID):
    myadmin = Admin.objects.get(adminID=adminID)
    myresident = Resident.objects.all().order_by('street').values()
    dict = {
        'myadmin':myadmin,
        'myresident':myresident
    }
    return render(request, 'admin_resident.html', dict)

# Admin register new resident_____________________________________________________________________________________
def adminregister_resident(request, adminID):
    if request.method == "GET":
        myadmin = Admin.objects.get(adminID=adminID)
        dict = {
            'myadmin':myadmin,
        }
        return render(request, 'adminregister_resident.html', dict)
    else:
        r_resID = request.POST['resID']
        r_resName = request.POST['resName']
        r_resIC = request.POST['resIC']
        r_resGender = request.POST['resGender']
        r_resRace = request.POST['resRace']
        r_resPhoneno = request.POST['resPhoneno']
        r_houseNo = request.POST['houseNo']
        r_street = request.POST['street']
        r_resPassword = request.POST['resPassword']
        r_address = r_houseNo + ", Jalan Kesuma " + r_street + ", Bandar Tasik Kesuma, 43700, Beranang, Selangor"
        newresident = Resident(resID=r_resID,resName=r_resName,resIC=r_resIC,resGender=r_resGender,resRace=r_resRace,resPhoneno=r_resPhoneno,houseNo=r_houseNo,street=r_street,address=r_address,resPassword=r_resPassword)
        newresident.save()
        url = reverse('admin_resident', kwargs={'adminID':adminID})
        return HttpResponseRedirect(url)    
    
# Admin update resident_______________________________________________________________________________________
def adminupdate_resident(request, adminID, resID):
    if request.method == "GET":
        myadmin = Admin.objects.get(adminID=adminID)
        myresident = Resident.objects.get(resID=resID)
        dict = {
            'myadmin':myadmin,
            'myresident':myresident
        }
        return render(request, 'adminupdate_resident.html', dict)
    else:
        myresident = Resident.objects.get(resID=resID)
        r_resName = request.POST['resName']
        r_resIC = request.POST['resIC']
        r_resGender = request.POST['resGender']
        r_resRace = request.POST['resRace']
        r_resPhoneno = request.POST['resPhoneno']
        r_houseNo = request.POST['houseNo']
        r_street = request.POST['street']
        r_resPassword = request.POST['resPassword']
        if (r_resName != ''):
            myresident.resName = r_resName
        if (r_resIC != ''):
            myresident.resIC = r_resIC
        if (r_resGender != ''):
            myresident.resGender = r_resGender
        if (r_resRace != ''):
            myresident.resRace = r_resRace
        if (r_resPhoneno != ''):
            myresident.resPhoneno = r_resPhoneno
        if (r_houseNo != ''):
            myresident.houseNo = r_houseNo
        if (r_street != ''):
            myresident.street = r_street
            myresident.address = r_houseNo + ", Jalan Kesuma " + r_street + ", Bandar Tasik Kesuma, 43700, Beranang, Selangor"
        if (r_resPassword != ''):
            myresident.resPassword = r_resPassword
        myresident.save()
        url = reverse('admin_resident', kwargs={'adminID':adminID})
        return HttpResponseRedirect(url)

# Admin delete resident______________________________________________________________________________________
def admindelete_resident(request, adminID, resID):
    if request.method == "POST":
        myadmin = Admin.objects.get(adminID=adminID)
        myresident = Resident.objects.get(resID=resID)
        myresident.delete()
        url = reverse('admin_resident', kwargs={'adminID':adminID})
        return HttpResponseRedirect(url)

# Admin guard_________________________________________________________________________________________________
def admin_guard(request, adminID):
    myadmin = Admin.objects.get(adminID=adminID)
    myguard = Guard.objects.annotate(numOfReport=Count('reportguard'))
    dict = {
        'myadmin':myadmin,
        'myguard':myguard,
    }
    return render(request, 'admin_guard.html', dict)

# Admin register new guard_____________________________________________________________________________________
def adminregister_guard(request, adminID):
    if request.method == "GET":
        myadmin = Admin.objects.get(adminID=adminID)
        dict = {
            'myadmin':myadmin,
        }
        return render(request, 'adminregister_guard.html', dict)
    else:
        g_guardID = request.POST['guardID']
        g_guardName = request.POST['guardName']
        g_guardPhoneno = request.POST['guardPhoneno']
        g_guardPost = request.POST['guardPost']
        g_guardShift = request.POST['guardShift']
        g_guardPassword = request.POST['guardPassword']
        newguard = Guard(guardID=g_guardID,guardName=g_guardName,guardPhoneno=g_guardPhoneno,guardPost=g_guardPost,guardShift=g_guardShift,guardPassword=g_guardPassword)
        newguard.save()
        url = reverse('admin_guard', kwargs={'adminID':adminID})
        return HttpResponseRedirect(url)
    
# Admin update guard___________________________________________________________________________________________
def adminupdate_guard(request, adminID, guardID):
    if request.method == "GET":
        myadmin = Admin.objects.get(adminID=adminID)
        myguard = Guard.objects.get(guardID=guardID)
        dict = {
            'myadmin':myadmin,
            'myguard':myguard
        }
        return render(request, 'adminupdate_guard.html', dict)
    else:
        myguard = Guard.objects.get(guardID=guardID)
        g_guardName = request.POST['guardName']
        g_guardPhoneno = request.POST['guardPhoneno']
        g_guardPost = request.POST['guardPost']
        g_guardShift = request.POST['guardShift']
        g_guardPassword = request.POST['guardPassword']
        if (g_guardName != ''):
            myguard.guardName = g_guardName
        if (g_guardPhoneno != ''):
            myguard.guardPhoneno = g_guardPhoneno
        if (g_guardPost != ''):
            myguard.guardPost = g_guardPost
        if (g_guardShift != ''):
            myguard.guardShift = g_guardShift
        if (g_guardPassword != ''):
            myguard.guardPassword = g_guardPassword
        myguard.save()
        url = reverse('admin_guard', kwargs={'adminID':adminID})
        return HttpResponseRedirect(url)
    
# Admin delete guard___________________________________________________________________________________________
def admindelete_guard(request, adminID, guardID):
    if request.method == "POST":
        myadmin = Admin.objects.get(adminID=adminID)
        myguard = Guard.objects.get(guardID=guardID)
        myguard.delete()
        url = reverse('admin_guard', kwargs={'adminID':adminID})
        return HttpResponseRedirect(url)

# Admin report_________________________________________________________________________________________________
def admin_report(request, adminID):
    myadmin = Admin.objects.get(adminID=adminID)
    myissue = ReportIssue.objects.all().order_by('-date').values()
    myguard = ReportGuard.objects.all().order_by('-date').values()
    dict = {
        'myadmin':myadmin,
        'myissue':myissue,
        'myguard':myguard
    }
    return render(request, 'admin_report.html', dict)

# Admin update issue___________________________________________________________________________________________
def adminupdate_issue(request, adminID, id):
    if request.method == "GET":
        myadmin = Admin.objects.get(adminID=adminID)
        myissue = ReportIssue.objects.get(id=id)
        dict = {
            'myadmin':myadmin,
            'myissue':myissue
        }
        return render(request, 'adminupdate_issue.html', dict)
    else:
        myissue = ReportIssue.objects.get(id=id)
        myadmin = Admin.objects.get(adminID=adminID)
        i_measuresTaken = request.POST['measuresTaken']
        if (i_measuresTaken != ''):
            myissue.measuresTaken = i_measuresTaken
            myissue.adminID = myadmin
            myissue.status = "Completed"
        myissue.save()
        url = reverse('admin_report', kwargs={'adminID':adminID})
        return HttpResponseRedirect(url)
    
# Admin update issue (in-progress)______________________________________________________________________________
def admininprogress_issue(request, adminID, id):
    if request.method == "POST":
        myadmin = Admin.objects.get(adminID=adminID)
        myissue = ReportIssue.objects.get(id=id)
        myissue.adminID = myadmin
        myissue.status = "In-progress"
        myissue.save()
        url = reverse('admin_report', kwargs={'adminID':adminID})
        return HttpResponseRedirect(url)
    
# Admin update report guard_______________________________________________________________________________________
def adminupdate_reportguard(request, adminID, id):
    if request.method == "GET":
        myadmin = Admin.objects.get(adminID=adminID)
        myissue = ReportGuard.objects.get(id=id)
        dict = {
            'myadmin':myadmin,
            'myissue':myissue
        }
        return render(request, 'adminupdate_reportguard.html', dict)
    else:
        myissue = ReportGuard.objects.get(id=id)
        myadmin = Admin.objects.get(adminID=adminID)
        i_measuresTaken = request.POST['measuresTaken']
        if (i_measuresTaken != ''):
            myissue.measuresTaken = i_measuresTaken
            myissue.adminID = myadmin
            myissue.status = "Completed"
        myissue.save()
        url = reverse('admin_report', kwargs={'adminID':adminID})
        return HttpResponseRedirect(url)
    
# Admin update report guard (in-progress)_______________________________________________________________________
def admininprogress_reportguard(request, adminID, id):
    if request.method == "POST":
        myadmin = Admin.objects.get(adminID=adminID)
        myissue = ReportGuard.objects.get(id=id)
        myissue.adminID = myadmin
        myissue.status = "In-progress"
        myissue.save()
        url = reverse('admin_report', kwargs={'adminID':adminID})
        return HttpResponseRedirect(url)

# Admin visitor_________________________________________________________________________________________________
def admin_visitor(request, adminID):
    myadmin = Admin.objects.get(adminID=adminID)
    myvisitor = Visitor.objects.all().order_by('-date').values()
    dict = {
        'myadmin':myadmin,
        'myvisitor':myvisitor,
    }
    return render(request, 'admin_visitor.html', dict)

# Admin event____________________________________________________________________________________________________
def admin_event(request, adminID):
    myadmin = Admin.objects.get(adminID=adminID)
    myevent = Event.objects.all().order_by('-date').values()
    dict = {
        'myadmin':myadmin,
        'myevent':myevent,
    }
    return render(request, 'admin_event.html', dict)