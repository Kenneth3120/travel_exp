from .models import Auditlog
from django.utils.timezone import now

def log_action(user, action, obj, changes=None):
    Auditlog.objects.create(
        user=user or "System",
        action=action,
        object_type=obj.__class__.__name__,
        object_id=obj.pk,
        object_repr=str(obj),
        timestamp=now(),
        changes=changes or {}
    )

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_tower_credential_types(tower_instance):
    """Fetches credential types from a given Ansible Tower instance."""
    url = tower_instance.url.rstrip('/') + '/api/v2/credential_types/'
    username = tower_instance.username
    password = tower_instance.password

    if not username or not password:
        raise ValueError(f"No credentials configured for Tower instance: {tower_instance.name}")

    try:
        response = requests.get(url, auth=(username, password), timeout=10, verify=False)
        response.raise_for_status()
        return response.json().get('results', [])
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Failed to connect to Tower instance {tower_instance.name}: {e}")

def create_tower_credential_type(tower_instance, credential_type_data):
    """Creates a credential type in a given Ansible Tower instance."""
    url = tower_instance.url.rstrip('/') + '/api/v2/credential_types/'
    username = tower_instance.username
    password = tower_instance.password

    if not username or not password:
        raise ValueError(f"No credentials configured for Tower instance: {tower_instance.name}")

    try:
        response = requests.post(url, auth=(username, password), json=credential_type_data, timeout=10, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Failed to create credential type in Tower instance {tower_instance.name}: {e}")

def get_tower_credential_type_by_name(tower_instance, credential_type_name):
    """Fetches a specific credential type by name from an Ansible Tower instance."""
    # Ansible Tower API to filter by name. Adjust if endpoint is different.
    url = tower_instance.url.rstrip('/') + f'/api/v2/credential_types/?name={credential_type_name}'
    username = tower_instance.username
    password = tower_instance.password

    if not username or not password:
        raise ValueError(f"No credentials configured for Tower instance: {tower_instance.name}")

    try:
        response = requests.get(url, auth=(username, password), timeout=10, verify=False)
        response.raise_for_status()
        results = response.json().get('results', [])
        # Assuming name is unique for credential types, return the first match
        return results[0] if results else None
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Failed to fetch credential type \'{credential_type_name}\' from Tower instance {tower_instance.name}: {e}")
