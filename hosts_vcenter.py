import sys
import requests
from urllib3 import disable_warnings

# Disable SSL Warnings
disable_warnings()


def _get_auth_token(host, user, pwd):
    # Build the Token request
    api_path = '/rest/com/vmware/cis/session'

    # Auth Token request
    result = requests.post(url=host + api_path, auth=(user, pwd), verify=False)

    # Check if we got a good result
    if result.status_code != 200:
        raise ValueError("Couldn't get a token, check your username or password.")

    # Return token value
    return result.json()["value"]


def _get_vm_data(host, auth_token):
    # Build the Data request
    api_path = '/rest/vcenter/vm'
    header = {"vmware-api-session-id": auth_token}

    # Return VM Data
    result = requests.get(url=host + api_path, headers=header, verify=False)

    # Check if we got a good result
    if result.status_code != 200:
        raise ValueError("Couldn't get the job data, status code: " + result.status_code())

    # Return vm data
    return result.json()["value"]


def get_hosts(host, user, pwd):
    try:
        # Get an auth token
        token = _get_auth_token(host, user, pwd)
        # Get the vm info
        vm_data = _get_vm_data(host, token)
    except ValueError as e:
        sys.exit(e)

    # Extract the Hostnames
    vm_hosts = []
    for vm in vm_data:
        vm_hosts.append(vm["name"])

    # Return the Hostname array
    return vm_hosts

