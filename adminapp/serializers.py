from rest_framework import serializers
# from rest_framework import Employees
from .models import Employees,AssignProducts,CustUser

class employeesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employees
        # fields = ['ename']
        fields = '__all__'


class assignSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssignProducts
        fields = ['id','employee_id','product_id']
        depth = 1

class signupSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustUser
        fields = ['username']
