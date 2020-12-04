from django.db import models
from django.contrib.auth.models import User
# Create your models here.
def to_upload(instance,filename):
   
    directory= os.path.join(settings.MEDIA_ROOT,instance.user.username)
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)
    directory_profile = os.path.join(directory,'ProfilePicture')
    try:
        os.stat(directory_profile)
    except:
        os.mkdir(directory_profile)
    return f"{instance.username}/ProfilePicture/{filename}"

def to_upload_company(instance,filename):
   
    directory= os.path.join(settings.MEDIA_ROOT,instance.Name)
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)
    directory_profile = os.path.join(directory,'ProfilePicture')
    try:
        os.stat(directory_profile)
    except:
        os.mkdir(directory_profile)
    return f"{instance.username}/ProfilePicture/{filename}"

class Profile(models.Model):

    user=models.OneToOneField(User,on_delete=models.CASCADE)
    Admin="Admin"
    Employee="Emp"
    Status_Choices=[
        (Admin,"Admin"),
        (Employee,"Employee")
    ]
    Status=models.CharField(max_length=10,choices=Status_Choices,default=None)
    ProfilePicture=models.ImageField(upload_to=to_upload,default="defaultprofile.jpg")
    Contact_number=models.CharField(max_length=20)
    Department=models.CharField(max_length=20)
    # temperature=models.ForeignKey('Temperature',on_delete=models.CASCADE)
    company=models.ForeignKey('Company',on_delete=models.CASCADE,default=None)
    
class Login(models.Model):
    timestamp=models.DateTimeField(auto_now_add=True)
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE)
    temperature=models.FloatField(default=0)
# class Temperature(models.Model):
#     reading=models.IntegerField() # Recording in Fahrenheit
#     timestamp=models.DateTimeField(auto_now_add=True)
#     user=models.ForeignKey(Profile,on_delete=models.CASCADE)

class Company(models.Model):
    Name=models.CharField(max_length=50)
    Logo=models.ImageField(upload_to=to_upload_company,default="defaultlogo.jpg")
    
    def __str__(self):
        return self.Name

class DailyBarGraph(models.Model):
    bar_graph=models.ImageField(upload_to="BarGraphs",blank=True)