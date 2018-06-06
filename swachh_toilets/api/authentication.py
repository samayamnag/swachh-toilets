from rest_framework import authentication
from rest_framework import exceptions
from django.conf import settings
import requests


class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        bearer_token = request.META.get('HTTP_AUTHORIZATION')
        if not bearer_token:
            return None

        url = f'{settings.AUTH_API_URL}users'
        headers = {
            'Accept': 'application/json;version=1.0',
            'Authorization': bearer_token
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user = response.json()['data']
            return (user, None)

        raise exceptions.AuthenticationFailed(response.json()['message'])


class Profile:

    def get_user_profile(self, request, profile_id):
        channel = request.GET.get('channel', 'swachhata-web')
        url = f'{settings.PROFILE_API_URL}{profile_id}?channel={channel}'
        bearer_token = request.META.get('HTTP_AUTHORIZATION')
        headers = {
            'Accept': 'application/json;version=1.0',
            'Authorization': bearer_token
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()['data']
