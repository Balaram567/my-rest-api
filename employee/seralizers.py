from rest_framework import serializers
from .import models
from django.contrib.auth import authenticate, login
from rest_framework import exceptions

class EmployeeSeralizer(serializers.ModelSerializer):
    class Meta:
        model=models.Question
        fields='__all__'

class LoginSeralizer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

    def validate(self, data):
        username=data.get("username")
        password=data.get("password")

        if username and password:
            user = authenticate(username="", password="")
            if user:
                if user.is_active():
                    data["user"]= user
                else:
                    msg="user is deactivated"
                    raise exceptions.ValidationError(msg)
            else:
                msg="unable to login with given credentials"
                raise exceptions.ValidationError(msg)
        else:
            msg="must provide username and password"
            raise exceptions.ValidationError(msg)
        return data