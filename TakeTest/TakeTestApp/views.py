from django.shortcuts import render
from rest_framework import mixins, pagination
from . import models, serializers, forms, utils, authentication
from django.views.generic import View
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, token_obtain_pair)
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer)
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from TakeTest import settings
import os
from datetime import  datetime
from django.utils import timezone


#######################################################################################################
###################################  Methods to handle UI Rendering ###################################
#######################################################################################################

def register(request):
    """
    To handle Register UI submission
    :param request: POST Request
    :return: UI Render
    """
    if request.method == 'POST':
        user = authentication.Authentication().create_account(
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            password=request.POST.get('password'))
        if user:
            return render(request, 'user_register.html', {"success":True})
    return render(request, 'user_register.html')

def login(request):
    """
    To handle Login UI submission
    :param request: POST Request
    :return: UI Render
    """
    if request.method == 'POST':
        user = authentication.Authentication().user_login(
            request=request,
            username=request.POST.get('username'),
            password=request.POST.get('password'))
        if user:
            return render(request, 'home.html', {"success": True})
        return render(request, 'user_signin.html', {"msg" : "Invalid credentials. Try Again.."})
    return render(request, 'user_signin.html')

def post_test(request):
    """
    To handle upload questions via UI
    :param request: POST Request
    :return:  UI Render
    """
    if request.method == 'POST':
        utils.BackendOperations().upload_test(request)
        return render(request, 'home.html', {"success": True})
    else:
        form = forms.UploadTestForm()
    return render(request, 'post_test.html', {
        'form': form
    })


######################################################################################################
########################################### Views for APIs ###########################################
######################################################################################################

class RegistrationView(GenericViewSet):
    """
    This class takes care of create user API
    """
    def create(self, request, *args, **kwargs):
        user = authentication.Authentication().create_account(
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            password=request.POST.get('password'))
        if user is not None:
            login(request)
            return Response("Registered & Logged in", status=status.HTTP_202_ACCEPTED)
        return Response("User Account creation failed", status=status.HTTP_401_UNAUTHORIZED)


class PostQuestionView(ModelViewSet):
    """
    This class takes care of uploading tests to DB
    """
    permission_classes = [IsAuthenticated]
    pagination_class = pagination.PageNumberPagination


    queryset = models.Tests.objects.all()
    serializer_class = serializers.TestsSerializer

    def perform_create(self, serializer):
        serializer.save(author_id = self.request.user.id)

    def get_queryset(self):  # get
        return models.Tests.objects.filter(author_id = self.request.user.id)

    def perform_destroy(self, instance):
        file_path = os.path.join(settings.MEDIA_ROOT, str(instance.test_file))
        os.remove(file_path)
        instance.delete()



class ReadyToAttendView(ModelViewSet):
    """
    This class takes care of tests ready to be taken
    """
    permission_classes = [IsAuthenticated]


    queryset = models.Tests.objects.all()
    serializer_class = serializers.ReadyToAttendSerializer

    def get_queryset(self):  # get
        return models.Tests.objects.filter(
            start_date__lte = datetime.now(tz=timezone.utc),
            end_date__gte= datetime.now(tz=timezone.utc),
            is_active=True).exclude(author_id=self.request.user.id)


class TakeTestView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Tests.objects.all()
    serializer_class = serializers.TakeTestSerializer


class AnswersView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PostAnswerSerializer
    queryset = models.Results.objects.all()

    def perform_create(self, serializer):
        serializer.save(user_id = self.request.user.id)



