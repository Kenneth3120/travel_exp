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
    login_view,
    logout_view
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
    path('user-info/', user_info),
    path('login/', login_view),
    path('logout/', logout_view),
]