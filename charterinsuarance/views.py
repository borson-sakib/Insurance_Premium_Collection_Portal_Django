from http.client import REQUEST_ENTITY_TOO_LARGE
from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import requests
from django.core.paginator import Paginator

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login
from django.contrib import messages
from datetime import date, datetime, timezone
import json
import os
from .utils import *
from charterinsuarance.models import Transaction, User
from django.db.models import Sum
url = "http://clicl.charteredlifebd.com:85/ApiCollection/"


  



def index(request):
    if "User_Email" in request.session :
        # print(datetime.now())
        return render(request,"home.html",  context=getUser(request.session["User_Email"]))
    else:
       return redirect('login')
    # s = requests.get("https://www.google.com/")
    # print(s)
    # return HttpResponse(s)
    
    # response=requests.post(url,data = data1)
    # print(response.json())
from django.views.decorators.csrf import csrf_exempt   
@csrf_exempt
def dataverify(request):
    context ={}
    if request.session.get("User_Email",False):
        if(request.method == 'GET'):
            return redirect('landing')
        if(request.method=="POST"):

            data1 = {}
            data1["USERID"] = "50154800"
            data1["POLICY"] = request.POST["policynum"]

            response=requests.post(url + "DataVerify",data = data1).json()

            # print(datetime.now())
            if(response[0]['CODE'] == "00"):
                context['name'] = response[0]['NAME']
                return JsonResponse( {"saas":"sasasa"})

def verify(request):
    context ={}
    if request.session.get("User_Email",True):
        context=getUser(request.session["User_Email"])
        if(request.method == 'GET'):
            return redirect('landing')
        if(request.method=="POST"):
            # print(request.POST)
            data1 = {}
            data1["USERID"] = "50154800"
            data1["POLICY"] = request.POST["policynum"]
            
            response=requests.post(url + "DataVerify",data = data1).json()

            
            if(response[0]['CODE'] == "00"):

                newtxn = Transaction(policy_no=request.POST["policynum"],
                                    amount=request.POST["amount"],
                                    payermobile_no=request.POST["payermobileno"],
                                    msg="S",

                                    )
                user = User.objects.get(email=request.session["User_Email"])
                newtxn.input_user= user
                newtxn.branch = user.branchname

                newtxn.save()

                txn_ID= Transaction.objects.get(id=newtxn.id)
                txn_ID.txn_id= str(date.today().strftime("%Y%m%d")) + "-" + str(newtxn.id).zfill(4)
                txn_ID.save()
                
                # print(newtxn.id)
                data2 = {}
                data2["USERID"] = "50154800"
                data2["PWD"] = "00x7yll33"
                data2["POLICY"] = request.POST["policynum"]
                data2["AMOUNT"] = request.POST["amount"]
                data2["PAYERMOBILENO"] = request.POST["payermobileno"]
                data2["PAYFORMOBILENO"] = data2["PAYERMOBILENO"]
                data2["BILLER_CODE"] = "130"
                data2["TXNID"] = txn_ID.txn_id
                data2["TXNDATE"] = str(newtxn.txn_date)
                data2["MSG"] = "S"

                # print(data2["TXNID"])
                response2=requests.post(url + "ApiCollection",data = data2).json()

                if(response2[0]['CODE'] == "00"):
                    txn = Transaction.objects.get(id=newtxn.id)
                    txn.status = True
                    txn.remarks = str(response2[0]['NAME'])
                    txn.save()
                    
                    # context['response'] = response2
                    context['message'] = 'Payement Successful'
                    context['classes'] = 'alert alert-success alert-dismissable'
                    context['txn'] = txn

                    return render(request, "verifiy.html", context=context)
                else:
                    txn1 = Transaction.objects.get(id=newtxn.id)
                    txn1.remarks = str(response2[0]['NAME'])
                    txn1.save() 
                    context["message"] = response2[0]["NAME"]
                    context['classes'] = 'alert alert-danger alert-dismissable'
                    return render(request, "verifiy.html",context=context)
                
                

            else:
                # messages.error(request,'Payement UNSuccessful')
                context["message"] = response[0]["NAME"]
                context['classes'] = 'alert alert-danger alert-dismissable'
                return render(request, "verifiy.html", context=context)

            
        else:
            return HttpResponse("failed")
    else:
       return redirect('login')

@login_required(login_url='/')
def txn_confirm(request):
    if(request.method=="POST"):
        return render(request, "txn_cnfrm.html")
    else:
        return HttpResponse("failed")


@login_required(login_url='/')
def txn_cnfrm_success(request):
    if(request.method=="POST"):

        data1 = {}
        data1["USERID"] = request.POST["userid"]
        data1["PWD"] = request.POST["pwd"]
        data1["POLICY"] = request.POST["policynum"]
        data1["AMOUNT"] = request.POST["amount"]
        data1["PAYERMOBILENO"] = request.POST["payermobileno"]
        data1["PAYFORMOBILENO"] = request.POST["payformobileno"]
        data1["BILLER_CODE"] = request.POST["billercode"]
        data1["TXNID"] = request.POST["txnid"]
        data1["TXNDATE"] = request.POST["txndate"]
        data1["MSG"] = request.POST["msg"]

        # print(data1)
        # {"USERID": "50154800", "POLICY": "0000060935"}
        response=requests.post(url + "ApiCollection",data = data1)
        print(response)
    
        return render(request, "verifiy.html", {'response': response.json()})
    else:
        return HttpResponse("failed")

@login_required(login_url='/')   
def txn_confrm_check(request):
    if(request.method=="POST"):
        return render(request, "txn_cnfrm.html")
    else:
        return HttpResponse("failed")

@login_required(login_url='/')
def txn_cnfrm_check_success(request):
    pass

   
def login(request):

    if request.method=="GET":
        return render(request, "registration\login.html")
    if request.method=="POST":
        domainmail = request.POST["username"]
        domainpass = request.POST["password"]
        domainmail = domainMailCheck(domainMail=domainmail)
        if ldapcheck(domainmail, domainpass):
            if checkAuthUser(domainmail):
                user = User.objects.get(email=domainmail)
                request.session['User_Email'] = user.email
                return redirect('landing')
            else:
                # return redirect('login')
                message = "Access Denied : You're Not Authorised !"
                return render( request, 'exceptions/val_error.html', {'err_message': message})
        else:
            message = "Invalid username or password"
            return render( request, 'exceptions/val_error.html', {'err_message': message})
            # return HttpResponse('<h1> vul password </h1> <h2>password: {}</h2> <h2> username {}</h2>'.format(domainpass, domainmail))

def logout(request):
    try:
        del request.session['User_Email']
    except KeyError:
        message = "Could not logout please try again"
        return render( request, 'exceptions/val_error.html', {'err_message': message})
    return redirect('login')


def register(request):
    if request.session.get("User_Email",True):
        user = User.objects.get(email=request.session["User_Email"])
        if user.is_staff():
            if request.method=="POST":
                email = request.POST['email']
                if "admin" in request.POST:
                    new_user = User.objects.create(email = email, is_admin=1)
                else:
                    new_user = User.objects.create(email = email)

                if "branch" not in request.POST:
                    message = "To create user, user must provide branch name."
                    return redirect('register', message=message)
                print(request.POST["branch"])
                branchObject = Branch.objects.get(branch_name=request.POST["branch"])
                new_user.branchname= branchObject
                new_user.save()


                
                message = " user {} creater successfully the users id is: {}".format(email, new_user.id)
                print(user)
                
                return render(request, "registration/register.html", context={'message':message, 'user_info':user,"branchlist":getBranchNameList() })
            context=getUser(request.session["User_Email"])
            context["branchlist"] = getBranchNameList()
            return render(request, "registration/register.html", context=context)
        # return HttpResponse("<h1> You are not admin!</h1>")  
        message = "Only admin privilaged individuals can do this operation"
        return render( request, 'exceptions/val_error.html', {'err_message': message})



def generate_report(request):
    if request.session.get("User_Email",True):
        context=getUser(request.session["User_Email"])

        if(context['user_info'].is_admin):
            queryset = Transaction.objects.all().order_by('-txn_date')
        else:
            queryset = Transaction.objects.filter(branch=context["user_info"].branchname, txn_date__date=datetime.today()).order_by('-txn_date')
        context["total_txn"] = len(queryset.filter(status=True))
        q = queryset.filter(status=True)
        context["sum"] = q.aggregate(Sum('amount'))["amount__sum"]
        context["date"] = datetime.today()
        context["branch_name"] = context["user_info"].branchname
        
        paginator = Paginator(queryset, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context["txns"] =page_obj
        # print(paginator.page_range())
        return render(request, "table_pages/txnlist.html", context=context)


def getUserProfile(request):
    
    context = getUser(request.session["User_Email"])
    
    return render(request, "userprofile/profile.html", context=context)

def postdatabydate(request):
    if request.session.get("User_Email",True):
        context=getUser(request.session["User_Email"])
        if "ajke" not in context:
            context["ajke"] =str(datetime.today()).split(' ')[0]
        # print(request.POST)
        if request.method =='GET':
            
            return render(request, "table_pages/datepicker.html", context= context)

        if request.method == 'POST':
            if "datesearch" in request.POST:
                date = request.POST["datesearch"]
                try:
                    day = datetime.strptime(date, "%Y-%m-%d").date()
                except Exception as e:
                    context["message"] = "Please enter a date in order for searching."
                    context['classes'] = 'alert alert-danger alert-dismissable'
                    return render(request, "table_pages/datepicker.html" , context=context) 
            else:
                day = datetime.today()
            
            # print(day)

            if(context['user_info'].is_admin):
                queryset = Transaction.objects.filter(txn_date__date=day).order_by('-txn_date')
            else:
                queryset = Transaction.objects.filter(branch=context["user_info"].branchname, txn_date__date=day).order_by('-txn_date')

            # queryset = Transaction.objects.filter(txn_date__date=day).order_by('-txn_date')
            # print(queryset)
            context["total_txn"] = len(queryset.filter(status=True))
            q = queryset.filter(status=True)
            context["sum"] = q.aggregate(Sum('amount'))["amount__sum"]
            # context["date"] = datetime.today()
            context["branch_name"] = context["user_info"].branchname

            paginator = Paginator(queryset, 20)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            context["txns"] =queryset
            context["date"] =day
            context["ajke"] =str(day).split(' ')[0]
            # print(paginator.page_range())

            return render(request, "table_pages/datepicker.html", context=context) 
    else:
        raise PermissionError

def reportWdatepicker(request):
    if request.session.get("User_Email",True):
        context=getUser(request.session["User_Email"])
        if "date" in request.GET:
            date = request.GET["date"]
            day = datetime.strptime(date, "%Y-%m-%d").date()
        else:
            day = datetime.today()
        
        print(day)
        queryset = Transaction.objects.filter(txn_date__date=day)
        print(queryset)

        paginator = Paginator(queryset, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context["txns"] =page_obj
        context["date"] =day
        # print(paginator.page_range())
        return render(request, "table_pages/datepicker.html", context=context)