from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import TowerInstance, Credential, ExecutionEnvironment, AuditLog


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']
        read_only_fields = ['id']


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'


class TowerInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TowerInstance
        exclude = []
        extra_kwargs = {
            'password': {'write_only': True}
        }


class CredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credential
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }


class ExecutionEnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutionEnvironment
        fields = '__all__'
