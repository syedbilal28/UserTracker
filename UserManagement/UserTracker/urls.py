from django.urls import path
from . import views
urlpatterns=[
    path('',views.index,name="index"),
    path('home/',views.home,name="home"),
    path('signup/',views.Signup,name="signup"),
    path('bargraph/',views.CurrentDayBar,name="CurrentDayBar"),
    path("daysbar/",views.DaysBar,name="DaysBar"),
    path("daysbarweek/",views.DaysBarWeek,name="DaysBarWeek"),
    path("Success/",views.Success,name="Success")
    # path('logout/',views.Logout,name="Logout"),
    
]