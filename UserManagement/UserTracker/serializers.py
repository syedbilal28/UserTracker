from rest_framework import serializers
from .models import Profile,Login
from django.contrib.auth.models import User 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","username","first_name"]


class ProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Profile
        fields=["user","Status","Department"]
class LoginSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    timestamp=serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:

        model=Login
        fields=["timestamp","profile","temperature"]