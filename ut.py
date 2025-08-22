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






@api_view(['GET'])
def credential_type_status(request):
    """Returns all CredentialTypes with their presence status across Tower instances."""
    # Retrieve all canonical CredentialTypes from our database
    db_credential_types = CredentialType.objects.all()
    instances = TowerInstance.objects.all()

    results = []

    for db_type in db_credential_types:
        type_status = {
            'id': db_type.id,
            'name': db_type.name,
            'description': db_type.description,
            'present_in_instances': [],
            'missing_in_instances': []
        }
        
        present_count = 0
        for instance in instances:
            try:
                # Attempt to get credential types from the Tower instance
                # This is a placeholder for actual API call to Ansible Tower
                # Need to implement a utility function for this
                tower_credential_types = get_tower_credential_types(instance)
                
                if db_type.name in [t.get('name') for t in tower_credential_types]:
                    type_status['present_in_instances'].append(instance.name)
                    present_count += 1
                else:
                    type_status['missing_in_instances'].append(instance.name)
            except Exception as e:
                # Handle connection errors or other issues with an instance
                print(f"Error fetching credential types from {instance.name}: {e}")
                type_status['missing_in_instances'].append(f"{instance.name} (Error: {e})")
                
        total_instances = len(instances)
        if total_instances > 0:
            percentage_present = (present_count / total_instances) * 100
            if percentage_present == 100:
                type_status['status'] = 'Green'
            elif percentage_present > 50:
                type_status['status'] = 'Orange'
            else:
                type_status['status'] = 'Red'
        else:
            type_status['status'] = 'N/A' # No instances configured
            
        results.append(type_status)

    return Response(results, status=status.HTTP_200_OK)

@api_view(['POST'])
def duplicate_missing_credential_type(request):
    """Duplicates a credential type to instances where it is missing."""
    credential_type_id = request.data.get('id')
    missing_in_instances = request.data.get('missing_in_instances', [])

    if not credential_type_id or not missing_in_instances:
        return Response({'message': 'Credential type ID and missing instances are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        db_credential_type = CredentialType.objects.get(id=credential_type_id)
    except CredentialType.DoesNotExist:
        return Response({'message': 'CredentialType not found.'}, status=status.HTTP_404_NOT_FOUND)

    results = []
    for instance_name in missing_in_instances:
        try:
            instance = TowerInstance.objects.get(name=instance_name)
            # Verify it's still missing before duplicating (to prevent race conditions)
            tower_credential_types = get_tower_credential_types(instance)
            if db_credential_type.name not in [t.get('name') for t in tower_credential_types]:
                # Prepare data for creating credential type in Tower
                credential_type_data = {
                    'name': db_credential_type.name,
                    'description': db_credential_type.description,
                    # Add other fields as necessary for Tower API
                }
                create_tower_credential_type(instance, credential_type_data)
                results.append({'instance': instance.name, 'status': 'duplicated'})
            else:
                results.append({'instance': instance.name, 'status': 'already_exists'})
        except TowerInstance.DoesNotExist:
            results.append({'instance': instance_name, 'status': 'instance_not_found'})
        except Exception as e:
            results.append({'instance': instance_name, 'status': 'error', 'message': str(e)})
            
    return Response(results, status=status.HTTP_200_OK)

@api_view(['POST'])
def verify_credential_type_by_name(request):
    """Verifies if a credential type exists under an alternative name in missing instances."""
    credential_type_id = request.data.get('id')
    alternative_name = request.data.get('alternative_name')
    missing_in_instances = request.data.get('missing_in_instances', [])

    if not credential_type_id or not alternative_name or not missing_in_instances:
        return Response({'message': 'Credential type ID, alternative name, and missing instances are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        db_credential_type = CredentialType.objects.get(id=credential_type_id)
    except CredentialType.DoesNotExist:
        return Response({'message': 'CredentialType not found.'}, status=status.HTTP_404_NOT_FOUND)

    results = []
    for instance_name in missing_in_instances:
        try:
            instance = TowerInstance.objects.get(name=instance_name)
            found_type = get_tower_credential_type_by_name(instance, alternative_name)
            if found_type:
                results.append({'instance': instance.name, 'status': 'found', 'found_name': found_type.get('name')})
            else:
                results.append({'instance': instance.name, 'status': 'not_found'})
        except TowerInstance.DoesNotExist:
            results.append({'instance': instance_name, 'status': 'instance_not_found'})
        except Exception as e:
            results.append({'instance': instance_name, 'status': 'error', 'message': str(e)})
            
    return Response(results, status=status.HTTP_200_OK)
