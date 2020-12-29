from rest_framework import serializers
from .models import Profile,Login,Customer
from django.contrib.auth.models import User 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","username","first_name","last_name","email"]


class ProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Profile
        fields=["user","company"]
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields=["first_name","last_name",'email',"Contact_number"]
class LoginSerializer(serializers.ModelSerializer):
    customer=CustomerSerializer()
    timestamp=serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:

        model=Login
        fields=["timestamp","customer","temperature"]