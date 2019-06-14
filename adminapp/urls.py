from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [

    url(r'^url/(?P<id>\d+)/$',views.product),
    path('login/',views.loginview),
    path('signup/',views.signupview),
    path('logout/',views.logoutview),
    path('',views.adminview),
    path('addproduct/',views.addproduct),
    path('viewproduct/',views.viewproduct),
    path('editproduct/',views.editproduct),
    path('addemployee/',views.addemployee),
    path('viewemployee/',views.viewemployee),
    # path('editemployee/',views.editemployee),
    url(r'^editemployee/(?P<id>\d+)/$',views.editemployee),
    url(r'^delemployee/(?P<id>\d+)/$',views.delemployee),
    path('assignproduct/',views.assignproduct),
    path('viewassignproduct/',views.viewassignproduct),
    path('employeesjson/',views.employeeList.as_view()),
    path('assignjson/',views.assignList.as_view()),
    path('usernames/',views.usernameList.as_view()),
    path('livesearch/',views.livesearch),
    path('forgotpassword/',views.forgotpassword),
    url(r'^(?P<userid>\d+)/(?P<otp>\d+)/$',views.recoverpassword),
    path('otpbutton/',views.otpbuttonview),
    # path('scanQR/',views.scanQR),
    # path('QRscan/',views.scanQR)

]