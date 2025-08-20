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


@api_view(['POST'])
def test_connection(request):
    """Tests connection to an AAP instance with provided credentials."""
    url = request.data.get('url')
    username = request.data.get('username')
    password = request.data.get('password')

    if not url or not username or not password:
        return Response({'message': 'URL, username, and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Ensure URL ends with a slash for API consistency, or adjust as needed for AAP
    test_url = url.rstrip('/') + '/api/v2/ping/' # Common AAP health check endpoint
    # test_url = url.rstrip('/') # or just the base URL if that's sufficient for a 'ping'

    try:
        # Using a small timeout to quickly check reachability
        response = requests.get(test_url, auth=(username, password), timeout=5, verify=False)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        return Response({'message': 'Connection successful!'}, status=status.HTTP_200_OK)
    except requests.exceptions.Timeout:
        return Response({'message': 'Connection timed out.'}, status=status.HTTP_408_REQUEST_TIMEOUT)
    except requests.exceptions.ConnectionError:
        return Response({'message': 'Could not connect to the AAP instance. Check the URL.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code in [401, 403]:
            return Response({'message': 'Authentication failed: Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': f'HTTP Error: {e.response.status_code} - {e.response.reason}'}, status=e.response.status_code)
    except Exception as e:
        return Response({'message': f'An unexpected error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
# Page no : 48-79, 
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
