from django.shortcuts import render
import requests
import urllib3

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
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
# Authentication Views
# -----------------------

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Login endpoint that returns JWT tokens"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            }
        })
    else:
        return Response(
            {'error': 'Invalid username or password'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Logout endpoint"""
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({'message': 'Logged out successfully'})
    except Exception as e:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


# -----------------------
# User Management
# -----------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]  # Only admins can perform CRUD


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    """Returns current user info for Angular frontend"""
    return Response({
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email,
        'role': request.user.role
    })


# Disable insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# -----------------------
# Tower Credential Proxy
# -----------------------
class TowerCredentialProxy(viewsets.ViewSet):
    """Proxies credential list calls to Ansible Tower using DB-stored credentials."""
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        old_instance = TowerInstance.objects.get(pk=serializer.instance.pk)
        new_instance = serializer.save()

        changes = {}
        for field in serializer.fields:
            old_val = getattr(old_instance, field, None)
            new_val = getattr(new_instance, field, None)
            if old_val != new_val:
                changes[field] = {'from': old_val, 'to': new_val}

        log_action(user=self.request.user.username, action='updated', obj=new_instance, changes=changes)

    def perform_create(self, serializer):
        instance = serializer.save()
        log_action(user=self.request.user.username, action='created', obj=instance)

    def perform_destroy(self, instance):
        log_action(user=self.request.user.username, action='deleted', obj=instance)
        instance.delete()


# -----------------------
# Credentials
# -----------------------
class CredentialViewSet(viewsets.ModelViewSet):
    queryset = Credential.objects.all()
    serializer_class = CredentialSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        old_instance = Credential.objects.get(pk=serializer.instance.pk)
        new_instance = serializer.save()

        changes = {}
        for field in serializer.fields:
            old_val = getattr(old_instance, field, None)
            new_val = getattr(new_instance, field, None)
            if old_val != new_val:
                changes[field] = {'from': old_val, 'to': new_val}

        log_action(user=self.request.user.username, action='updated', obj=new_instance, changes=changes)

    def perform_create(self, serializer):
        instance = serializer.save()
        log_action(user=self.request.user.username, action='created', obj=instance)

    def perform_destroy(self, instance):
        log_action(user=self.request.user.username, action='deleted', obj=instance)
        instance.delete()


# -----------------------
# Execution Environments
# -----------------------
class ExecutionEnvironmentViewSet(viewsets.ModelViewSet):
    queryset = ExecutionEnvironment.objects.all()
    serializer_class = ExecutionEnvironmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        old_instance = ExecutionEnvironment.objects.get(pk=serializer.instance.pk)
        new_instance = serializer.save()

        changes = {}
        for field in serializer.fields:
            old_val = getattr(old_instance, field, None)
            new_val = getattr(new_instance, field, None)
            if old_val != new_val:
                changes[field] = {'from': old_val, 'to': new_val}

        log_action(user=self.request.user.username, action='updated', obj=new_instance, changes=changes)

    def perform_create(self, serializer):
        instance = serializer.save()
        log_action(user=self.request.user.username, action='created', obj=instance)

    def perform_destroy(self, instance):
        log_action(user=self.request.user.username, action='deleted', obj=instance)
        instance.delete()


# -----------------------
# Audit Logs
# -----------------------
class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all().order_by('-timestamp')
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]