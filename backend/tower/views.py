from django.shortcuts import render
import requests
import urllib3

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model

from .models import TowerConfig, TowerInstance, Credential, ExecutionEnvironment, AuditLog
from .serializers import (
    TowerInstanceSerializer,
    CredentialSerializer,
    ExecutionEnvironmentSerializer,
    AuditLogSerializer,
    UserSerializer
)
from .utils import log_action
from .permissions import IsAdmin, ReadOnlyForViewer

User = get_user_model()

# -----------------------
# User Management
# -----------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]  # Only admins can perform CRUD


@api_view(['GET'])
def user_info(request):
    """Returns current user info for Angular frontend"""
    if not request.user.is_authenticated:
        return Response({'detail': 'Not authenticated'}, status=401)

    return Response({
        'username': request.user.username,
        'role': request.user.role
    })


# Disable insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# -----------------------
# Tower Credential Proxy
# -----------------------
class TowerCredentialProxy(viewsets.ViewSet):
    """Proxies credential list calls to Ansible Tower using DB-stored credentials."""

    def list(self, request):
        cfg = TowerConfig.objects.first()
        if not cfg:
            return Response(
                {"detail": "TowerConfig not configured."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        tower_url = cfg.base_url.rstrip('/') + '/api/v2/credentials/'
        try:
            resp = requests.get(
                tower_url,
                auth=(cfg.username, cfg.password),
                timeout=10,
                verify=False
            )
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("Tower proxy error:", e)
            return Response(
                {"detail": f"Error contacting Tower: {e}"},
                status=status.HTTP_502_BAD_GATEWAY
            )

        results = resp.json().get('results', [])
        return Response(results)


# -----------------------
# Tower Instance
# -----------------------
class TowerInstanceViewSet(viewsets.ModelViewSet):
    queryset = TowerInstance.objects.all()
    serializer_class = TowerInstanceSerializer

    def perform_update(self, serializer):
        old_instance = TowerInstance.objects.get(pk=serializer.instance.pk)
        new_instance = serializer.save()

        changes = {}
        for field in serializer.fields:
            old_val = getattr(old_instance, field, None)
            new_val = getattr(new_instance, field, None)
            if old_val != new_val:
                changes[field] = {'from': old_val, 'to': new_val}

        log_action(user='admin', action='updated', obj=new_instance, changes=changes)

    def perform_create(self, serializer):
        instance = serializer.save()
        log_action(user='admin', action='created', obj=instance)

    def perform_destroy(self, instance):
        log_action(user='admin', action='deleted', obj=instance)
        instance.delete()


# -----------------------
# Credentials
# -----------------------
class CredentialViewSet(viewsets.ModelViewSet):
    queryset = Credential.objects.all()
    serializer_class = CredentialSerializer

    def perform_update(self, serializer):
        old_instance = Credential.objects.get(pk=serializer.instance.pk)
        new_instance = serializer.save()

        changes = {}
        for field in serializer.fields:
            old_val = getattr(old_instance, field, None)
            new_val = getattr(new_instance, field, None)
            if old_val != new_val:
                changes[field] = {'from': old_val, 'to': new_val}

        log_action(user='admin', action='updated', obj=new_instance, changes=changes)

    def perform_create(self, serializer):
        instance = serializer.save()
        log_action(user='admin', action='created', obj=instance)

    def perform_destroy(self, instance):
        log_action(user='admin', action='deleted', obj=instance)
        instance.delete()


# -----------------------
# Execution Environments
# -----------------------
class ExecutionEnvironmentViewSet(viewsets.ModelViewSet):
    queryset = ExecutionEnvironment.objects.all()
    serializer_class = ExecutionEnvironmentSerializer

    def perform_update(self, serializer):
        old_instance = ExecutionEnvironment.objects.get(pk=serializer.instance.pk)
        new_instance = serializer.save()

        changes = {}
        for field in serializer.fields:
            old_val = getattr(old_instance, field, None)
            new_val = getattr(new_instance, field, None)
            if old_val != new_val:
                changes[field] = {'from': old_val, 'to': new_val}

        log_action(user='admin', action='updated', obj=new_instance, changes=changes)

    def perform_create(self, serializer):
        instance = serializer.save()
        log_action(user='admin', action='created', obj=instance)

    def perform_destroy(self, instance):
        log_action(user='admin', action='deleted', obj=instance)
        instance.delete()


# -----------------------
# Audit Logs
# -----------------------
class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all().order_by('-timestamp')
    serializer_class = AuditLogSerializer
