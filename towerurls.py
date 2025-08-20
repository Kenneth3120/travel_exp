from django.urls import path, include
from rest_framework.routers import DefaultRouter
# 11-12, 28
from .views import (
    TowerInstanceViewSet,
    CredentialViewSet,
    ExecutionEnvironmentViewSet,
    AuditLogViewSet,
    TowerCredentialProxy,
    UserViewSet,
    user_info,
    test_connection
)

router = DefaultRouter()

router.register(r'tower-credentials', TowerCredentialProxy, basename='tower-credentials')
router.register(r'tower', TowerInstanceViewSet, basename='tower')
router.register(r'instances', TowerInstanceViewSet, basename='instance')
router.register(r'credentials', CredentialViewSet)
router.register(r'environments', ExecutionEnvironmentViewSet)
router.register(r'audit-logs', AuditLogViewSet)
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('api/user-info/', user_info),
    path('api/test-connection/', test_connection),
]
