from django.shortcuts import render,redirect
from .models import Profile,Login,DailyBarGraph
from django.contrib.auth.models import User
from django.contrib.auth import login, logout,authenticate
from .forms import LoginForm,SignupForm,ProfileForm
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
            temperature=form.cleaned_data["temperature"]
            user=authenticate(request,username=username,password=password)
            
            if user is not None:
                login(request,user)
                profile=Profile.objects.get(user=user)
                Login.objects.create(profile=profile,temperature=temperature)
               
                if profile.Status== "Emp":
                    return redirect('Success')
                else:
                    return redirect('home')
    else:

        form = LoginForm()
        return render(request,'index.html',{"form":form})

def Signup(request):
    if request.method=="POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            Profile.objects.create()
            return redirect('index') 
    else:
        form = SignupForm()
        form_1=ProfileForm()
    return render(request,"signup.html", {"form":form,"form_1":form_1})
    
def home(request):
    if request.user.profile.Status=="Admin":
        pd.set_option('display.max_colwidth', -1)
        login_last_10=Login.objects.all().order_by('-timestamp')
        
        login_last_10_data=LoginSerializer(login_last_10,many=True).data
        
        login_last_10_df=pd_json.json_normalize(login_last_10_data)
        login_last_10_df=login_last_10_df.rename(columns={
            "profile.user.id":"ID",
            "profile.user.email":"Email Address",
            "profile.user.last_name":"Last Name",
            "profile.user.username":"Username",
            "profile.user.first_name":"First Name",
            "profile.Status":"Status",
            "profile.Department":"Department",
            "timestamp":"Check In Time",
            "temperature":"Temperature",
            "profile.Contact_number":"Contact Number"
            })
        login_last_10_df=login_last_10_df.drop("ID",axis=1)
        login_last_10_df=login_last_10_df[["Check In Time","Username","First Name","Last Name","Contact Number","Department","Status","Temperature"]]
        login_last_10_table=login_last_10_df.to_html(justify="center",index=False)
        context={"table":login_last_10_table}
        return render(request,"home.html",context)
        # login_count=Login.objects.filter(timestamp__lte=datetime.now())
@csrf_exempt
def CurrentDayBar(request):
    # print("from form",request.POST.get("starting_date"))
    with verrou:
        print("from form",request.POST.get("starting_date"))
        try:
            current_date=datetime.strptime(request.POST.get("starting_date"),"%d-%m-%Y").date()
        except:
            current_date=datetime.now(pytz.timezone("America/Grenada")).date() 
        l=Login.objects.filter(timestamp__date=current_date)
        dict_time={}
        for i in range(24):
            if i==0:
                i="00"
            dict_time[str(i)]=0
        len_login=len(l)
        for i in range(len_login):
            try:
                dict_time[str(l[i].timestamp.hour)]+=1
            except:
                pass
        
        objects = list(dict_time.keys())
        y_pos = np.arange(len(objects))
        performance = list(dict_time.values())
        
        i=i+1
        plt.figure(i,figsize=(11,4))
        plt.bar(y_pos, performance, align='center', alpha=0.5,color=["#56bb2a"])
        plt.xticks(y_pos, objects)
        plt.ylabel('Logins',color="#56bb2a")
        plt.title('Logins per hour',color="#56bb2a")
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
            current_date=datetime.strptime(request.POST.get("starting_date"),"%d-%m-%Y").date()
        except:
            current_date=datetime.now(pytz.timezone("America/Grenada")).date() 
        # current_date=datetime.now(pytz.timezone("America/Grenada")).date()
        dates=[]
        for i in range(6,0,-1):
            dates.append(current_date- timedelta(days=i))
        dates.append(current_date)
        print(dates)
        l=Login.objects.filter(timestamp__date__in=dates)
        dict_ref={}
        len_l=len(l)
       
        for i in range(7):
            dict_ref[str(dates[i])]=0

        for i in range(len_l):
            try:
                dict_ref[str(l[i].timestamp.date())] +=1
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
        plt.ylabel('Logins',color="#56bb2a")
        plt.title('Logins Per Day Over a week',color="#56bb2a")
        f = io.BytesIO()
        plt.savefig(f,format="png")
        plt.close()
        f.seek(0)
        string=base64.b64encode(f.read())
        url=urllib.parse.quote(string)
        return JsonResponse({"data":url},safe=False)
    # return render(request,"test.html",{"data":url})
@csrf_exempt
def DaysBarWeek(request):
    with verrou:
        try:
            current_date=datetime.strptime(request.POST.get("starting_date"),"%d-%m-%Y").date()
        except:
            current_date=datetime.now(pytz.timezone("America/Grenada")).date() 
        # current_date=datetime.now(pytz.timezone("America/Grenada")).date() 
        dates=[]
        for i in range(29,0,-1):
            dates.append(current_date- timedelta(days=i))
        dates.append(current_date)
        print(dates)
        l=Login.objects.filter(timestamp__date__in=dates)
        dict_ref={}
        len_l=len(l)
        for i in range(30):
            dict_ref[str(dates[i])]=0
      
        for i in range(len_l):
            try:
                dict_ref[str(l[i].timestamp.date())] +=1
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
        plt.ylabel('Logins',color="#56bb2a")
        plt.title('Logins per Day Over a Month',color="#56bb2a")
        f = io.BytesIO()
        plt.savefig(f,format="png")
        plt.close()
        f.seek(0)
        string=base64.b64encode(f.read())
        url=urllib.parse.quote(string)
        return JsonResponse({"data":url},safe=False)
    # return render(request,"test.html",{"data":url})    
def Success(request):
        return render(request,'success.html')