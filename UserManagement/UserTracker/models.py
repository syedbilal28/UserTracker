from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ImageDraw
import qrcode
from io import BytesIO
from django.core.files import File
import os
from django.conf import settings

# Create your models here.

def to_upload_company(instance,filename):
   
    directory= os.path.join(settings.MEDIA_ROOT,instance.Name)
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)
    
    return f"{instance.Name}/{filename}"

class Profile(models.Model):

    user=models.OneToOneField(User,on_delete=models.CASCADE)
    company=models.ForeignKey('Company',on_delete=models.CASCADE,default=None)
    active=models.BooleanField(default=False)
    
class Customer(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30,blank=True,null=True)
    Contact_number=models.CharField(max_length=20)
    email=models.EmailField()
    address=models.CharField(max_length=200,default=None,blank=True,null=True)
class Login(models.Model):
    timestamp=models.DateTimeField(auto_now_add=True)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    temperature=models.FloatField(default=0)
    company=models.ForeignKey('Company',on_delete=models.CASCADE)

class Company(models.Model):
    Name=models.CharField(max_length=50)
    Logo=models.ImageField(upload_to=to_upload_company,default="defaultlogo.jpg",blank=True,null=True)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    
    def __str__(self):
        return self.Name
     

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(f"http://127.0.0.1:8000/company/{self.pk}/checkin")
        canvas = Image.new('RGB', (370, 370), 'white')
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.Name}.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)

# class DailyBarGraph(models.Model):
#     bar_graph=models.ImageField(upload_to="BarGraphs",blank=True)

# class Website(models.Model):
#     name = models.CharField(max_length=200)
#     qr_code = models.ImageField(upload_to='qr_codes', blank=True)

#     def __str__(self):
#         return str(self.name)

#     def save(self, *args, **kwargs):
#         qrcode_img = qrcode.make(self.name)
#         canvas = Image.new('RGB', (290, 290), 'white')
#         canvas.paste(qrcode_img)
#         fname = f'qr_code-{self.name}.png'
#         buffer = BytesIO()
#         canvas.save(buffer,'PNG')
#         self.qr_code.save(fname, File(buffer), save=False)
#         canvas.close()
#         super().save(*args, **kwargs)