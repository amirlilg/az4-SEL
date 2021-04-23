import hashlib
import random
import string

import django.db
import django.utils.timezone as timezone
from django.contrib.sites import requests
from django.http import HttpResponse

from account.models import User

admin = User()
admin.username, admin.password, admin.email, admin.isAdmin, admin.profile = 'admin', hashlib.md5(
    '12341234'.encode('utf-8')).digest(), 'admin@site.com', True, 'I AM ADMIN!'
admin.save()

signup_tries = 0
login_tries = 0
profile_tries = 0


class Signup(viewsets.ViewSet):
    def handle_request(self, request):
        user = User()
        data = request.data
        try:
            user.username, user.password, user.email = data['username'], hashlib.md5(
                data['password'].encode('utf-8')).digest(), data['email']
            try:
                user.save()
            except django.db.utils.IntegrityError:
                return HttpResponse('User exists', status=409)
        except KeyError:
            return HttpResponse('Input error', status=406)
        return HttpResponse('Signup done', status=200)


class Login(viewsets.ViewSet):
    def handle_request(self, request):
        try:
            username, password = request.data['username'], str(request.data['password'])
        except KeyError:
            return HttpResponse('Input error', status=406)
        user = User.objects.get(username=username)
        if str(user.password) == str(hashlib.md5(password.encode('utf-8')).digest()):
            if user.token_exp_time > django.utils.timezone.now():
                return HttpResponse(user.token, status=200)
            else:
                user.token = ''.join(random.choices(string.ascii_lowercase + string.digits, k=70))
                user.token_expire = timezone.now() + timezone.timedelta(hours=2)
                user.save()
                return HttpResponse(user.token, status=200)
        else:
            return HttpResponse("Authentication error", status=403)


class Profile(viewsets.ViewSet):
    def handle_request(self, request):
        try:
            token = request.data['token']
        except KeyError:
            return HttpResponse('Input error', status=406)

        user = User.objects.get(token=token)
        if not user:
            return HttpResponse('Token isn\'t valid', status=409)

        if user.token_expire < django.utils.timezone.now():
            return HttpResponse('Token expired', status=409)

        if 'profile' in request.data:
            user.profile = request.data['profile']
            user.save()

        return HttpResponse('Your profile changed to: ' + user.profile, status=200)


class Gateway(viewsets.ViewSet):
    def handle_request(self, request):
        try:
            service = request.data["service"]
        except KeyError:
            return HttpResponse('Bad Request', status=400)
        if service == 'signup':
            if signup_tries < 3:
                return self.signup(request.data)
            else:
                return HttpResponse('Service Unavailable', status=503)

        if service == 'login':
            if login_tries < 3:
                return self.login(request.data)
            else:
                return HttpResponse('Service Unavailable', status=503)

        if service == 'profile':
            if profile_tries < 3:
                return self.profile(request.data)
            else:
                return HttpResponse('Service Unavailable', status=503)
        return HttpResponse('Bad Request', status=400)

    @staticmethod
    def signup(data):
        global signup_tries
        url = 'http://127.0.0.1:8000/signup'
        response = get_response(url, data)
        if response.status_code >= 500:
            signup_tries += 1
            return HttpResponse('Service Unavailable', status=503)
        return HttpResponse(response.text, status=response.status_code)

    @staticmethod
    def login(data):
        global login_tries
        url = 'http://127.0.0.1:8000/login'
        response = get_response(url, data)
        if response.status_code >= 500:
            login_tries += 1
            return HttpResponse('Service Unavailable', status=503)
        return HttpResponse(response.text, status=response.status_code)

    @staticmethod
    def profile(data):
        global profile_tries
        url = 'http://127.0.0.1:8000/profile'
        response = get_response(url, data)
        if response.status_code >= 500:
            profile_tries += 1
            return HttpResponse('Service Unavailable', status=503)
        return HttpResponse(response.text, status=response.status_code)


def get_response(url, data):
    try:
        return requests.post(url, data=data, timeout=0.5)
    except:
        return HttpResponse('Service Unavailable', status=503)
