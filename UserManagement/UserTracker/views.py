from django.shortcuts import render,redirect,HttpResponse
from .models import Profile,Login,Company,Customer
from django.contrib.auth.models import User
from django.contrib.auth import login, logout,authenticate
from .forms import LoginForm,SignupForm,CustomerForm,ProfileForm
import pandas as pd
from datetime import datetime,date,timedelta
from .serializers import LoginSerializer
import pandas.io.json as pd_json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
import io
from django.core.files.images import ImageFile
import random
import numpy as np
import urllib,base64
from django.http import JsonResponse
import pytz
import random
from threading import RLock
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
verrou = RLock()
# Create your views here.

i=0

def index(request):
    if request.method=="POST":
        print("POSTED")
        form = LoginForm(data=request.POST)
        print(form)
        if form.is_valid():
            
            username=form.cleaned_data["username"]
            password=form.cleaned_data["password"]
            
            user=authenticate(request,username=username,password=password)
            if user.profile.active==False:
                request.session["message"]="Account not active yet"
                return redirect('index')
            if user is None:
                request.session["message"]="Invalid username or password"
                return redirect('index')
            if user is not None:
                request.session["message"]=""
                login(request,user)
                profile=Profile.objects.get(user=user)
                
                return redirect('home')
    else:
        try:
            message=request.session.get("message")
        except:
            message=""
        form = LoginForm()
        return render(request,'index.html',{"form":form,"message":message})
@csrf_exempt
def Checkin(request,company_id):
    company =Company.objects.get(pk=int(company_id))
    if request.method=="POST":
        print(request.POST)
        form=CustomerForm(request.POST)
        if form.is_valid():

            try:
                first_name=form.cleaned_data["first_name"]
                last_name=form.cleaned_data["last_name"]
                email=form.cleaned_data["email"]
                customer=Customer.objects.get(email=email)
                if len(request.POST.get("notes")) >0:
                    notes=request.POST.get("notes")
                    customers_list= notes.split(" ")
                    l=len(customers_list)
                    for i in range(0,l,2):
                        first_name=customers_list[i]   
                        temperature=customers_list[i+1]
                        extra_customer=Customer.objects.create(
                            first_name=first_name,
                            last_name="",
                            email=customer.email,
                            Contact_number=customer.Contact_number,
                            address=customer.address
                        )  
                    Login.objects.create(customer=extra_customer,temperature=temperature,company=company)        
            except:
                customer=form.save()
                if len(request.POST.get("notes")) >0:
                    notes=request.POST.get("notes")
                    customers_list= notes.split(" ")
                    l=len(customers_list)
                    for i in range(0,l,2):
                        first_name=customers_list[i]   
                        temperature=customers_list[i+1]
                        extra_customer=Customer.objects.create(
                            first_name=first_name,
                            last_name="",
                            email=customer.email,
                            Contact_number=customer.Contact_number,
                            address=customer.address
                        )
                        Login.objects.create(customer=extra_customer,temperature=temperature,company=company)
            temperature=request.POST.get("temperature")
            Login.objects.create(customer=customer,temperature=temperature,company=company)

            return redirect('index')
    else:
        form=CustomerForm()
        company=Company.objects.get(pk=company_id)
        return render(request,"checkin_test.html",{"form":form,"Company":company})

def Signup(request):
    if request.method=="POST":
        form = SignupForm(request.POST)
        form_1= ProfileForm(request.POST)
        if form.is_valid() and form_1.is_valid():
            user=form.save()
            Profile.objects.create(user=user,company=form_1.cleaned_data["company"])
            return HttpResponse(status=200) 
    else:
        form = SignupForm()
        form_1=ProfileForm()
    return render(request,"signup.html", {"form":form,"form_1":form_1})


@login_required    
def home(request):
    # if request.user.profile.Status=="Admin":
    pd.set_option('display.max_colwidth', -1)
    login_last_10=Login.objects.filter(company=request.user.profile.company).order_by('-timestamp')
    l=len(login_last_10)
    login_last_10=list(login_last_10)
    # for i in range(l):
    #     if login_last_10[i].profile.company!=request.user.profile.company:
    #         login_last_10.remove(i)
    login_last_10_data=LoginSerializer(login_last_10,many=True).data
    print(login_last_10_data)
    login_last_10_df=pd_json.json_normalize(login_last_10_data)
    print(login_last_10_df)
    login_last_10_df=login_last_10_df.rename(columns={
        # "customer.id":"ID",
        "customer.email":"Email Address",
        "customer.last_name":"Last Name",
        
        "customer.first_name":"First Name",
        "customer.address":"Address",
        "timestamp":"Check In Time",
        "temperature":"Temperature",
        "customer.Contact_number":"Contact Number"
        })
    # login_last_10_df=login_last_10_df.drop("ID",axis=1)
    try:
        login_last_10_df=login_last_10_df[["Check In Time","First Name","Last Name","Email Address","Contact Number","Temperature"]]
    except:
        login_last_10_df-login_last_10_df
    login_last_10_table=login_last_10_df.to_html(justify="center",index=False)
    context={"table":login_last_10_table,"Company":request.user.profile.company}
    return render(request,"home.html",context)
        # login_count=Login.objects.filter(timestamp__lte=datetime.now())
@csrf_exempt
def CurrentDayBar(request):
    # print("from form",request.POST.get("starting_date"))
    with verrou:
        print("from form",request.POST.get("starting_date"))
        try:
            current_date=datetime.strptime(request.POST.get("starting_date"),"%Y-%m-%d").date()
        except:
            current_date=datetime.now(pytz.timezone("America/Grenada")).date() 
        login_data=Login.objects.filter(timestamp__date=current_date)
        login_data=login_data.filter(company=request.user.profile.company)
        l=len(login_data)
        login_data=list(login_data)
        # for i in range(l):
        #     if login_data[i].profile.company!=request.user.profile.company:
        #         login_data.remove(i)
        dict_time={}
        for i in range(24):
            if i==0:
                i="00"
            dict_time[str(i)]=0
        len_login=len(login_data)
        for i in range(len_login):
            try:
                dict_time[str(login_data[i].timestamp.hour)]+=1
            except:
                pass
        
        objects = list(dict_time.keys())
        y_pos = np.arange(len(objects))
        performance = list(dict_time.values())
        
        i=i+1
        plt.figure(i,figsize=(11,4))
        plt.bar(y_pos, performance, align='center', alpha=0.5,color=["#56bb2a"])
        plt.xticks(y_pos, objects)
        plt.ylabel('Checkins',color="#56bb2a")
        plt.title('Checkins per hour',color="#56bb2a")
        f = io.BytesIO()
        plt.savefig(f,format="png")
        plt.close()
        f.seek(0)
        string=base64.b64encode(f.read())
        url=urllib.parse.quote(string)
        return JsonResponse({"data":url},safe=False)
    # return render(request,"test.html",{"data":url})

@csrf_exempt
def DaysBar(request):
    with verrou:
        try:
            starting_date=datetime.strptime(request.POST.get("starting_date"),"%Y-%m-%d").date()
            end_date=datetime.strptime(request.POST.get("end_date"),"%Y-%m-%d").date()
        except:
            starting_date=datetime.now(pytz.timezone("America/Grenada")).date() 
            end_date=datetime.now(pytz.timezone("America/Grenada")).date() + timedelta(days=7)
        # current_date=datetime.now(pytz.timezone("America/Grenada")).date()
        dates=[]
        x=starting_date
        y=0
        # for i in range(6,0,-1):
        #     dates.append(starting_date- timedelta(days=i))
        while x < end_date:
            dates.append(starting_date + timedelta(days=y))
            y+=1
            x=x+timedelta(days=1)
        dates.append(starting_date)
        print(dates)
        login_data=Login.objects.filter(timestamp__date__in=dates)
        login_data=login_data.filter(company=request.user.profile.company)
        l=len(login_data)
        login_data=list(login_data)
        # for i in range(l):
        #     if login_data[i].profile.company!=request.user.profile.company:
        #         login_data.remove(i)
        dict_ref={}
        len_l=len(login_data)
       
        for i in range(7):
            dict_ref[str(dates[i])]=0

        for i in range(len_l):
            try:
                dict_ref[str(login_data[i].timestamp.date())] +=1
            except:
                pass
        
        dict_num_to_weekday={
                "0":"Mon",
                "1":"Tues",
                "2":"Wed",
                "3":"Thurs",
                "4":"Fri",
                "5":"Sat",
                "6":"Sun"
            }
        dict_new={}
        for key in dict_ref:
            dict_new[datetime.strptime(key,"%Y-%m-%d").weekday()]=dict_ref[key]
        dict_final={}
        for key in dict_new:
            dict_final[dict_num_to_weekday[str(key)]]=dict_new[key]
        print(dict_final.keys())
       
        objects = list(dict_final.keys())
        y_pos = np.arange(len(objects))
        performance = list(dict_final.values())
        
        i=i+1
        plt.figure(i)
        plt.bar(y_pos, performance, align='center', alpha=0.5,color=["#56bb2a"])
        plt.xticks(y_pos,objects)
        plt.ylabel('Checkins',color="#56bb2a")
        plt.title('Checkins Per Day Over a week',color="#56bb2a")
        f = io.BytesIO()
        plt.savefig(f,format="png")
        plt.close()
        f.seek(0)
        string=base64.b64encode(f.read())
        url=urllib.parse.quote(string)
        return JsonResponse({"data":url},safe=False)
#     # return render(request,"test.html",{"data":url})
@csrf_exempt
def DaysBarWeek(request):
    with verrou:
        try:
            starting_date=datetime.strptime(request.POST.get("starting_date"),"%Y-%m-%d").date()
            end_date=starting_date+timedelta(days=30)
        except:
            starting_date=datetime.now(pytz.timezone("America/Grenada")).date() 
            end_date=datetime.now(pytz.timezone("America/Grenada")).date() + timedelta(days=30)
        # current_date=datetime.now(pytz.timezone("America/Grenada")).date() 
        dates=[]
        # for i in range(29,0,-1):
        #     dates.append(current_date- timedelta(days=i))
        # dates.append(current_date)
        x=starting_date
        y=0
        # for i in range(6,0,-1):
        #     dates.append(starting_date- timedelta(days=i))
        while x < end_date:
            print(y)
            dates.append(starting_date + timedelta(days=y))
            y+=1
            x=x+timedelta(days=1)
        # print(len(dates))
        login_data=Login.objects.filter(timestamp__date__in=dates)
        login_data=login_data.filter(company=request.user.profile.company)
        l=len(login_data)
        login_data=list(login_data)
        # for i in range(l):
        #     if login_data[i].profile.company!=request.user.profile.company:
        #         login_data.remove(i)
        dict_ref={}
        len_l=len(login_data)
        for i in range(30):
            dict_ref[str(dates[i])]=0
      
        for i in range(len_l):
            try:
                dict_ref[str(login_data[i].timestamp.date())] +=1
            except:
                pass
        objects = list(dict_ref.keys())
        y_pos = np.arange(len(objects))
        performance = list(dict_ref.values())
        
        i=i+2
        plt.figure(i)

        plt.plot(y_pos, performance, alpha=0.5, color = "#56bb2a")
        plt.xticks(ticks=[y_pos[0],y_pos[-1]],labels=[objects[0],objects[-1]])
        # plt.xticks([objects[0],objects[-1]], visible=True, rotation="horizontal")
        plt.ylabel('Checkins',color="#56bb2a")
        plt.title('Checkins per Day Over a Month',color="#56bb2a")
        f = io.BytesIO()
        plt.savefig(f,format="png")
        plt.close()
        f.seek(0)
        string=base64.b64encode(f.read())
        url=urllib.parse.quote(string)
        return JsonResponse({"data":url},safe=False)
    # return render(request,"test.html",{"data":url})    
# def Success(request):
#         return render(request,'success.html')
def HowItWorks(request):
    return render(request,"howitworks.html")

def qrcode(request):
    qr_code=request.user.profile.company.qr_code.path
    to_send=qr_code.split('\\')[-3:]
    print(to_send)
    path=""
    for i in to_send:
        path+=i+"/"
    print(path)

    return render(request,"qrcode.html",{"qrcode":path[:-1]})
def SignupRequests(request):
    unsigned_profiles=Profile.objects.filter(active=False)
    context={"Unsigned_Profiles":unsigned_profiles}
    return render(request,"signuprequests.html",context)
@csrf_exempt
def GiveRightsUser(request):
    try:
        request.user.profile
        return redirect(index) 
    except:
        profile_id=request.POST.get("profile_id")
        try:
            profile=Profile.objects.get(pk=profile_id)

            profile.active=True
            profile.save()
        except:
            profile_id=None
        return JsonResponse({"profile_id":profile_id},status=200)
