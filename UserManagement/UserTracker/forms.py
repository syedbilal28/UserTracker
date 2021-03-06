from django import forms
from django.contrib.auth.models import User
from .models import Profile,Customer,Login
class CustomerForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields="__all__"
        
class LoginForm(forms.Form):
    username=forms.CharField(max_length=50,label='Username',label_suffix='',widget=forms.TextInput(attrs={"id":"username"}))
    
    password=forms.CharField(max_length=50,label='Password',label_suffix='',widget=forms.PasswordInput(attrs={"id":"password"}))
    
class SignupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=[
            'first_name',
            'last_name',
            'username',
            'email',
            
            'password',
            
        ]
    def save(self,commit=True):
        user = super(SignupForm,self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=[
            "company",
            "contact_number"
            ]
