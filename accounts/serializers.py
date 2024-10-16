from rest_framework import serializers
from django.core.validators import MinLengthValidator
from .models import UserModel
from utils import ORGANIZATION, BRANCH, ROLE

class UserSerializer(serializers.ModelSerializer):
    organization = serializers.ChoiceField(choices=ORGANIZATION, help_text='Select user organization')
    branch = serializers.ChoiceField(choices=BRANCH, help_text='Select user branch')
    role = serializers.ChoiceField(choices=ROLE, help_text='Assign role to user.')
    
    class Meta:
        model = UserModel
        fields = ['id', 'first_name', 'last_name', 'organization', 'branch', 'role', 'email', 'password', 'is_active']
        extra_kwargs = {'id': {'read_only': True}, 'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UpdateSerializer(serializers.ModelSerializer):
    organization = serializers.ChoiceField(choices=ORGANIZATION, help_text='Select user organization')
    branch = serializers.ChoiceField(choices=BRANCH, help_text='Select user branch')
    role = serializers.ChoiceField(choices=ROLE, help_text='Assign role to user.')
    
    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'organization', 'branch', 'role', 'is_active']


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    

class PasswordConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(validators=[MinLengthValidator(6)])
