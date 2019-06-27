from . import models
from django.contrib.auth import authenticate, login

class Authentication():
    def __init__(self):
        pass
    def create_account(self, username, email, password):
        new_user = models.Users.objects.create_user(
            username=username,
            email=email,
            password=password)
        new_user.save()
        user = authenticate(username=username, password=password)
        if user:
            return user
        return None

    def user_login(self, request, username, password):
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return user
        return None

