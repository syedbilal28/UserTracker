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
# Create your views here.

def index(request):
    if request.method=="POST":
        print("POSTED")
        form = LoginForm(data=request.POST)
        print(form)
        if form.is_valid():
            
            username=form.cleaned_data["username"]
            password=form.cleaned_data["password"]
            
            user=authenticate(request,username=username,password=password)
            
            if user is not None:
                login(request,user)
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
        login_last_10=Login.objects.all().order_by('-timestamp')[:10]
        login_last_10_data=LoginSerializer(login_last_10,many=True).data
        
        login_last_10_df=pd_json.json_normalize(login_last_10_data)
        login_last_10_df=login_last_10_df.rename(columns={
            "profile.user.id":"ID",
            "profile.user.username":"Username",
            "profile.user.first_name":"First Name",
            "profile.Status":"Status",
            "profile.Department":"Department",
            "timestamp":"Time",
            "temperature":"Temperature"
            })
        login_last_10_df=login_last_10_df.drop("ID",axis=1)
        login_last_10_df=login_last_10_df[["Time","Username","First Name","Department","Status","Temperature"]]
        login_last_10_table=login_last_10_df.to_html(justify="center",index=False)
        context={"table":login_last_10_table}
        return render(request,"home.html",context)
        # login_count=Login.objects.filter(timestamp__lte=datetime.now())
def CurrentDayBar(request):
    l=Login.objects.filter(timestamp__date=datetime.now(pytz.timezone("America/Grenada")).date())
    dict_time={}
    for i in range(24):
        if i==0:
            i="00"
        dict_time[str(i)]=0
    len_login=len(l)
    for i in range(len_login):
        dict_time[str(l[i].timestamp.hour)]+=1
    objects = list(dict_time.keys())
    y_pos = np.arange(len(objects))
    performance = list(dict_time.values())

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Logins')
    plt.title('Logins per hour')
    f = io.BytesIO()
    plt.savefig(f,format="png")
    plt.close()
    f.seek(0)
    string=base64.b64encode(f.read())
    url=urllib.parse.quote(string)
    # return JsonResponse({"data":url},safe=False)
    return render(request,"test.html",{"data":url})

def DaysBar(request):
    current_date=datetime.now(pytz.timezone("America/Grenada")).date() 
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
    print(dict_ref)
    for i in range(len_l):
        dict_ref[str(l[i].timestamp.date())] +=1
    
    objects = list(dict_ref.keys())
    y_pos = np.arange(len(objects))
    performance = list(dict_ref.values())

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Logins')
    plt.title('Logins per hour')
    f = io.BytesIO()
    plt.savefig(f,format="png")
    plt.close()
    f.seek(0)
    string=base64.b64encode(f.read())
    url=urllib.parse.quote(string)
    return render(request,"test.html",{"data":url})
    
    