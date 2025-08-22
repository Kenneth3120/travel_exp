from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    TowerInstanceViewSet,
    CredentialViewSet,
    ExecutionEnvironmentViewSet,
    AuditLogViewSet,
    TowerCredentialProxy,
    UserViewSet,
    user_info,
    test_connection,
    CredentialTypeViewSet,
    credential_type_status,
    duplicate_missing_credential_type,
    verify_credential_type_by_name
)

router = DefaultRouter()

router.register(r'tower-credentials', TowerCredentialProxy, basename='tower-credentials')
router.register(r'tower', TowerInstanceViewSet, basename='tower')
router.register(r'instances', TowerInstanceViewSet, basename='instance')
router.register(r'credentials', CredentialViewSet)
router.register(r'environments', ExecutionEnvironmentViewSet)
router.register(r'audit-logs', AuditLogViewSet)
router.register(r'users', UserViewSet, basename='user')
router.register(r'credential-types', CredentialTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/user-info/', user_info),
    path('api/test-connection/', test_connection),
    path('api/credential-type-status/', credential_type_status),
    path('api/duplicate-credential-type/', duplicate_missing_credential_type),
    path('api/verify-credential-type/', verify_credential_type_by_name),
]
