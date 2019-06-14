from django.shortcuts import render,HttpResponse,HttpResponseRedirect,loader
from . import models
from email.mime.text import MIMEText
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail,EmailMessage
from assetmanagement import settings
from django.db import IntegrityError
import qrcode
import random
import socket
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . models import Employees,AssignProducts
from . serializers import employeesSerializer,assignSerializer,signupSerializer
import cv2
import threading


class employeeList(APIView):

    def get(self,request):
        employees1 = Employees.objects.all()
        serializer = employeesSerializer(employees1, many = True)
        return Response(serializer.data)

    def post(self):
        pass

class assignList(APIView):

    def get(self,request):
        assi = AssignProducts.objects.all()
        serializer = assignSerializer(assi, many = True)
        return Response(serializer.data)

    def post(self):
        pass

class usernameList(APIView):

    def get(self,request):
        usernames = get_user_model().objects.all()
        serializer = signupSerializer(usernames, many = True)
        return Response(serializer.data)

    def post(self):
        pass

qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
# Create your views here.

def loginview(request):
    template = loader.get_template('login.html')
    msg=''
    msgtype = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is None:
            msg = 'Invalid Login Details'
            msgtype = 'danger'
        elif user.is_phone_verified!=1 and user.is_email_verifiel!=1:
            msg = 'Mobile Number and Email is not Verified'
            msgtype = 'warning'
        elif user.is_phone_verified!=1:
            msg = 'Mobile Number is not Verified'
            msgtype = 'warning'
        elif user.is_email_verifiel!=1:
            msg = 'Email not Verified'
            msgtype = 'warning'
        else:
            login(request,user)
            return HttpResponseRedirect('/')
    return HttpResponse(template.render({'msg':msg,'type':msgtype},request))

def signupview(request):
    template=loader.get_template('signup.html')
    if request.method == 'POST':
        user = get_user_model()
        user.objects.create_user(username=request.POST.get('username'),email=request.POST.get('email'), password=request.POST.get('password'),mobile_number = request.POST.get('phone'))
        return HttpResponse(loader.get_template('redirectpage.html').render({},request))
    return HttpResponse(template.render({},request))

@login_required(login_url='/login/')
def adminview(request):
    template = loader.get_template('adminview.html')
    products=models.Products.objects.all()
    employees=models.Employees.objects.all()
    assignproducts=models.AssignProducts.objects.all()
    msg=''
    # check=False
    # print('aaaaaaaaaaaaaaaaaaaaaaaaa',check)
    if request.method=='POST' and 'stophere' in request.POST:
        dcheck = models.Check.objects.get(id=1)
        dcheck.check = True
        dcheck.save()
    if request.method =='POST' and 'QR' in request.POST:
        dcheck = models.Check.objects.get(id=1)
        dcheck.check = False
        dcheck.save()
        cap = cv2.VideoCapture(0)
        mins = 0
        while (True):
            dcheck = models.Check.objects.filter(check=True)
            if len(dcheck)>0:
                break
            # print('dddddddddddddddddddddddddddddddddddddddddddddddddddddd',dcheck)
            # print('dddddddddddddddddddddddd',check)
            ret, frame = cap.read()
            inputImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            qrDecoder = cv2.QRCodeDetector()
            data, bbox, rectifiedImage = qrDecoder.detectAndDecode(inputImage)
            mins += 1
            if len(data) > 0:
                print("Decoded Data : {}".format(data))
                break
            # if mins==280:
            #     check=True
            #     break
        cap.release()
        cv2.destroyAllWindows()
        # if check==True:
        #     return HttpResponseRedirect('/')
        try:
            assignproduct = models.AssignProducts.objects.get(product_id=data)
            return HttpResponse(loader.get_template('viewQR.html').render({'assign': assignproduct}, request))
        except:
            msg = 'invalid'



    return HttpResponse(template.render({ 'pno': len(products),'eno' : len(employees),'ano':len(assignproducts),'msg':msg },request))

@login_required(login_url='/login/')
def addproduct(request):
    template = loader.get_template('products/addproduct.html')
    if request.method == 'POST':
        p_regi = models.Products()
        p_regi.pname = request.POST.get('pname')
        p_regi.pdescription=request.POST.get('pdescription')
        p_regi.pcategory=request.POST.get('pcategory')
        p_regi.punits=request.POST.get('punits')

        p_regi.save()



        # qr.add_data(p_regi.id)
        # qr.make(fit=True)
        # img = qr.make_image()
        # a=str(p_regi.id)
        # img.save("qr_" + a +".jpg" )

        # p_regi.qrcode = qr.add_data(p_regi.id)
        # p_regi.save()
        
        img = qrcode.make(p_regi.id)
        a = str(p_regi.id)
        img.save("qr_" + a + ".jpg")

        return HttpResponseRedirect('/viewproduct/')
    return HttpResponse(template.render({},request))

@login_required(login_url='/login/')
def viewproduct(request):
    template = loader.get_template('products/viewproduct.html')
    p_regi = models.Products.objects.all()
    if request.method == 'POST' and 'dltbtn' in request.POST:
        product=models.Products.objects.get(id=request.POST.get('dltbtn'))
        product.delete()
    return HttpResponse(template.render({'products': p_regi}, request))

@login_required(login_url='/login/')
def editproduct(request):
    template= loader.get_template('products/editproduct.html')
    if request.method == 'POST' and 'edt' in request.POST:
        p_regi = models.Products.objects.get(id=request.POST.get('edt'))
        p_regi.pname = request.POST.get('pname')
        p_regi.pdescription = request.POST.get('pdescription')
        p_regi.pcategory = request.POST.get('pcategory')
        p_regi.punits = request.POST.get('punits')
        p_regi.save()
        return HttpResponseRedirect('/viewproduct/')
    p_regi = models.Products.objects.get(id=request.POST.get('edtbtn'))
    return HttpResponse(template.render({'products': p_regi}, request))

@login_required(login_url='/login/')
def addemployee(request):
    template = loader.get_template('employees/addemployee.html')
    if request.method == 'POST':
        p_regi = models.Employees()
        p_regi.ename = request.POST.get('ename')
        p_regi.eage=request.POST.get('eage')
        p_regi.save()
        return HttpResponseRedirect('/viewemployee/')
    return HttpResponse(template.render({},request))

@login_required(login_url='/login/')
def viewemployee(request):
    template = loader.get_template('livesearch.html')
    # e_regi = models.Employees.objects.all()
    # if request.method == 'POST' and 'dltbtn' in request.POST:
    #     employee=models.Employees.objects.get(id=request.POST.get('dltbtn'))
    #     employee.delete()
    return HttpResponse(template.render({}, request))

def livesearch(request):
    template = loader.get_template('livesearch.html')
    e_regi = models.Employees.objects.all()
    if request.method == 'POST' and 'dltbtn' in request.POST:
        employee=models.Employees.objects.get(id=request.POST.get('dltbtn'))
        employee.delete()
    return HttpResponse(template.render({'emp':e_regi}, request))

def product(request,id):
    template=loader.get_template('products/product.html')
    product=models.Products.objects.get(id=id)
    return HttpResponse(template.render({'product':product},request))

@login_required(login_url='/login/')
def editemployee(request,id):
    template= loader.get_template('employees/editemployee.html')
    if request.method == 'POST' and 'edt' in request.POST:
        e_regi = models.Employees.objects.get(id=request.POST.get('edt'))
        e_regi.ename = request.POST.get('ename')
        e_regi.eage = request.POST.get('eage')
        e_regi.save()
        return HttpResponseRedirect('/viewemployee/')
    e_regi = models.Employees.objects.get(id=id)
    return HttpResponse(template.render({'employee': e_regi}, request))

@login_required(login_url='/login/')
def delemployee(request,id):
    e_regi = models.Employees.objects.get(id=id)
    e_regi.delete()
    return HttpResponseRedirect('/viewemployee/')

@login_required(login_url='/login/')
def assignproduct(request):
    template = loader.get_template('assignproducts/assignproduct.html')
    msg=''
    color = 'red'
    if request.method == 'POST':
        pcheck = models.Products.objects.filter(id=request.POST.get('pid'))
        echeck = models.Employees.objects.filter(id=request.POST.get('eid'))
        pascheck=models.AssignProducts.objects.filter(product_id=request.POST.get('pid'))
        if len(pcheck)==0:
            msg = 'Invalid Product ID'
        elif len(echeck)==0:
            msg = 'Invalid Employee ID'
        elif len(pascheck)==0:
            regi = models.AssignProducts()
            regi.employee_id = models.Employees.objects.get(id=request.POST.get('eid'))
            regi.product_id = models.Products.objects.get(id=request.POST.get('pid'))
            regi.save()
            msg='Product Assigned Successfully'
            color='green'
        else:
            msg = 'Product Already Assigned'
    return HttpResponse(template.render({ 'msg' : msg, 'color' : color}, request))

@login_required(login_url='/login/')
def viewassignproduct(request):
    template = loader.get_template('assignproducts/viewassignproduct.html')
    regi = models.AssignProducts.objects.all()
    if request.method == 'POST' and 'qrgenerate' in request.POST:
        assignproduct=models.AssignProducts.objects.get(id=request.POST.get('qrgenerate'))

        # qr.add_data(assignproduct.product_id.id)
        # qr.make(fit=True)
        # img = qr.make_image()

        img = qrcode.make(assignproduct.product_id.id)
        a = str(assignproduct.product_id.id)
        img.save("qr/qr_" + a + ".jpg")

    if request.method == 'POST' and 'dltbtn' in request.POST:
        assignproduct=models.AssignProducts.objects.get(id=request.POST.get('dltbtn'))
        assignproduct.delete()
    return HttpResponse(template.render({'assignproduct': regi}, request))

@login_required(login_url='/login/')
def logoutview(request):
    logout(request)
    return HttpResponseRedirect('/')

def forgotpassword(request):
    template = loader.get_template('forgotpassword.html')
    msg=''
    color=''
    smsg=''
    usr = ''
    if request.method == 'POST' and 'resend' in request.POST:
        try:
            username = request.POST.get('username2')
            User = models.CustUser.objects.get(username=username)
            otp_db = models.Otp.objects.get(user_id=User.id)

            def otpsenting(user):
                subject = 'Action Required'
                from_email = settings.EMAIL_HOST_USER
                email = user.email
                otp = otp_db.token
                message = 'Click this link to recover your email.\n\n http://127.0.0.1:8000/' + str(user.id) + '/' + str(
                    otp) + '/'
                send_mail(subject=subject, from_email=from_email, message=message, recipient_list=(email,),
                          fail_silently=False)



            def otp_btn_email(user):
                subject = "Password Reset"
                otp = otp_db.token

                link= 'http://127.0.0.1:8000/' + str(user.id) + '/' + str(otp) + '/'
                data= loader.get_template('otpbutton.html')
                content = data.render({'name':user.username,'link':link,})
                from_email = settings.EMAIL_HOST_USER
                to=user.email
                msg = EmailMessage(subject, content, from_email, [to])
                msg.content_subtype = "html"  # Main content is now text/html
                msg.send()

            otp_btn_email(User)

        except socket.gaierror:
            smsg="gaiError"

    if request.method == 'POST' and 'mainform' in request.POST:
        username = request.POST.get('username')
        def otpsenting(user):
            subject = 'Action Required'
            from_email = settings.EMAIL_HOST_USER
            email = user.email
            otp = random.randint(10000, 99999)
            otp_db = models.Otp()
            otp_db.user = models.CustUser.objects.get(username=user.username)
            otp_db.token = otp
            otp_db.save()
            message = 'Click this link to recover your email.\n\n http://127.0.0.1:8000/' + str(user.id) + '/' + str(
                otp)+'/'
            send_mail(subject=subject, from_email=from_email, message=message, recipient_list=(email,),
                      fail_silently=False)

        try:
            user=models.CustUser.objects.get(username=username)
            otpsenting(user)
            msg='Recover link sent to mail'
            color='white'
        except models.CustUser.DoesNotExist:
            msg = 'Invalid Username'
            color ='red'
        except IntegrityError:
            smsg='intError'
            usr = request.POST.get("username")
        except socket.gaierror:
            smsg='gaiError'

    return HttpResponse(template.render({'msg':msg,'color':color,'smsg':smsg ,'usr':usr},request))

def recoverpassword(request,userid,otp):
    template = loader.get_template('newpassword.html')
    otp=models.Otp.objects.get(token=otp,user_id=userid)
    user_id=otp.user_id
    user_db=models.CustUser.objects.get(id=user_id)
    smsg=''
    msg=''
    if request.method=='POST':
        password=request.POST.get('password')
        againpassword=request.POST.get('password2')
        if password == againpassword:
            user_db.set_password(againpassword)
            user_db.save()
            otp.delete()
            smsg='success'
        else:
            msg='password not matching'
    # return HttpResponseRedirect('/')
    return HttpResponse(template.render({'msg':msg,'smsg':smsg},request))

def otpbuttonview(request):
    return HttpResponse(loader.get_template('redirectpage.html').render({}, request))


'''
def scanQR(request):
    stopscan=''
    if request.method == "POST":
        stopscan = request.POST.get('stopscan')

    data=0
    msg = ''
    assignproduct=''
    check='scanning'
    cap = cv2.VideoCapture(0)
    print('asdfasdfasdf',stopscan)
    while (True):
        ret, frame = cap.read()
        check='scanning'
        inputImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        qrDecoder = cv2.QRCodeDetector()
        data, bbox, rectifiedImage = qrDecoder.detectAndDecode(inputImage)
        if stopscan=="true":
            break
        elif len(data) > 0:
            print("Decoded Data : {}".format(data))
            break

    cap.release()
    cv2.destroyAllWindows()

    try:
        assignproduct=models.AssignProducts.objects.get(product_id=data)
    except:
        msg='Invalid QR code'
    print('aaaaaaaaaaaa',assignproduct)
    return HttpResponse(loader.get_template('viewQR.html').render({'assign':assignproduct,'msg':msg,'check':check}, request))'''



# def scanQR(request):
#     return {'check':'scanning'}
    # return HttpResponse(loader.get_template('adminview.html').render({'check':'scanning'}, request))


# def scanQR(request):
#     scanQR2()
#     scanQR3(request)