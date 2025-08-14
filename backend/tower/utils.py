from .models import Auditlog
from django.utils.timezone import now

def log_action(user, action, obj):
    Auditlog.objects.create(
        user=user or "System",
        action=action,
        object_type=obj.__class__.__name__,
        object_id=obj.pk,
        object_repr=str(obj),
        timestamp=now(),
        changes=changes or {}
    )