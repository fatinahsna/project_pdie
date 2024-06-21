from django.urls import path
from . import views

urlpatterns = [
    #==========================================RESIDENT==================================================
    path('', views.resident_loginpage, name='resident_login'),
    path('residentlogin', views.resident_login, name='resident_login'),
    path('residentdashboard/<str:resID>', views.resident_dashboard, name='resident_dashboard'),
    path('residentregistration/<str:resID>', views.resident_registration, name='resident_registration'),
    path('residentregistration/registervisitor/<str:resID>', views.register_visitor, name='register_visitor'),
    path('residentregistration/registerevent/<str:resID>', views.register_event, name='register_event'),
    path('residentregistration/qrcode/<str:resID>', views.resident_qrcode, name='resident_qrcode'),
    path('residentregistration/updateevent/<str:resID>/<str:id>', views.update_event, name='update_event'),
    path('residentregistration/deleteevent/<str:resID>/<str:id>', views.delete_event, name='delete_event'),
    path('residentreport/<str:resID>', views.resident_report, name='resident_report'),
    path('residentreport/reportissue/<str:resID>', views.report_issue, name='report_issue'),
    path('residentreport/updateissue/<str:resID>/<str:id>', views.update_issue, name='update_issue'),
    path('residentreport/deleteissue/<str:resID>/<str:id>', views.delete_issue, name='delete_issue'),
    path('residentreport/reportguard/<str:resID>', views.report_guard, name='report_guard'),
    path('residentreport/updatereportguard/<str:resID>/<str:id>', views.update_guard, name='update_guard'),
    path('residentreport/deletereportguard/<str:resID>/<str:id>', views.delete_guard, name='delete_guard'),
    path('residentguard/<str:resID>', views.resident_guard, name='resident_guard'),

    #==========================================GUARD=====================================================
    path('guardloginpage', views.guard_loginpage, name='guard_login'),
    path('guardlogin', views.guard_login, name='guard_login'),
    path('guarddashboard/<str:guardID>', views.guard_dashboard, name='guard_dashboard'),
    path('guardvisitor/<str:guardID>', views.guard_visitor, name='guard_visitor'),
    path('guardvisitor/filteredvisitor/<str:guardID>', views.guardfilter_visitor, name='guardfilter_visitor'),
    path('guardvisitor/registervisitor/<str:guardID>', views.guardregister_visitor, name='guardregister_visitor'),
    path('guardvisitor/visitordetails/<str:guardID>/<str:id>', views.guarddetails_visitor, name='guarddetails_visitor'),
    path('guardvisitor/visitorcheckin/<str:guardID>/<str:id>', views.guardcheckin_visitor, name='guardcheckin_visitor'),
    path('guardvisitor/visitorcheckout/<str:guardID>/<str:id>', views.guardcheckout_visitor, name='guardcheckout_visitor'),
    path('guardevent/<str:guardID>', views.guard_event, name='guard_event'),
    path('guardreport/<str:guardID>', views.guard_report, name='guard_report'),
    path('guardreport/reportissue/<str:guardID>', views.guardreport_issue, name='guardreport_issue'),
    path('guardreport/updateissue/<str:guardID>/<str:id>', views.guardupdate_issue, name='guardupdate_issue'),
    path('guardreport/deleteissue/<str:guardID>/<str:id>', views.guarddelete_issue, name='guarddelete_issue'),

    #==========================================ADMIN=====================================================
    path('admindashboard/<str:adminID>', views.admin_dashboard, name='admin_dashboard'),
    path('adminresident/<str:adminID>', views.admin_resident, name='admin_resident'),
    path('adminresident/registerresident/<str:adminID>', views.adminregister_resident, name='adminregister_resident'),
    path('adminresident/updateresident/<str:adminID>/<str:resID>', views.adminupdate_resident, name='adminupdate_resident'),
    path('adminresident/deleteresident/<str:adminID>/<str:resID>', views.admindelete_resident, name='admindelete_resident'),
    path('adminguard/<str:adminID>', views.admin_guard, name='admin_guard'),
    path('adminguard/registerguard/<str:adminID>', views.adminregister_guard, name='adminregister_guard'),
    path('adminguard/updateguard/<str:adminID>/<str:guardID>', views.adminupdate_guard, name='adminupdate_guard'),
    path('adminguard/deleteguard/<str:adminID>/<str:guardID>', views.admindelete_guard, name='admindelete_guard'),
    path('adminreport/<str:adminID>', views.admin_report, name='admin_report'),
    path('adminreport/updateissue/<str:adminID>/<str:id>', views.adminupdate_issue, name='adminupdate_issue'),
    path('adminreport/inprogress/<str:adminID>/<str:id>', views.admininprogress_issue, name='admininprogress_issue'),
    path('adminreport/updatereportguard/<str:adminID>/<str:id>', views.adminupdate_reportguard, name='adminupdate_reportguard'),
    path('adminreport/inprogressreportguard/<str:adminID>/<str:id>', views.admininprogress_reportguard, name='admininprogress_reportguard'),
    path('adminvisitor/<str:adminID>', views.admin_visitor, name='admin_visitor'),
    path('adminevent/<str:adminID>', views.admin_event, name='admin_event'),
]