from django.urls import path
from . import views
urlpatterns=[
    path('',views.index,name="index"),
    path('home/',views.home,name="home"),
    path('signup/',views.Signup,name="signup"),
    path('bargraph/',views.CurrentDayBar,name="CurrentDayBar")
    # path('logout/',views.Logout,name="Logout"),
    
]