import sys
import requests
from urllib3 import disable_warnings

# Disable SSL Warnings
disable_warnings()


def _get_auth_token(host, username, password):
    # Build the Token request
    api_path = '/api/oauth2/token'
    header = {'x-api-version': '1.0-rev1', "Content-Type": 'application/x-www-form-urlencoded'}

    data = {
        "grant_type": "password",
        "username": username,
        "password": password
    }

    # Auth Token request
    result = requests.post(url=host + api_path, data=data, headers=header, verify=False)

    # Check if we got a good result
    if result.status_code != 200:
        raise ValueError("Couldn't get a token, check your username or password.")

    # Return the token
    return result.json()["access_token"]


def _get_job_data(host, auth_token):
    # build the request
    api_path = '/api/v1/jobs'
    header = {'x-api-version': '1.0-rev1', "accept": "application/json", "Authorization": "Bearer " + auth_token}

    # Get the job data
    result = requests.get(url=host + api_path, headers=header, verify=False)

    # Check if we got a good result
    if result.status_code != 200:
        raise ValueError("Couldn't get the job data, status code: "+result.status_code())

    # Return the job data
    return result.json()["data"]


def get_hosts(host, username, password):
    try:
        # Get access token
        token = _get_auth_token(host, username, password)
        # Get job data
        data = _get_job_data(host, token)
    except ValueError as e:
        sys.exit(e)

    # Extract the Hostnames
    job_hosts = []
    for jobs in data:
        for obj in jobs["virtualMachines"]["includes"]:
            job_hosts.append(obj["inventoryObject"]["name"])

    # Return the Hostnames
    return job_hosts

