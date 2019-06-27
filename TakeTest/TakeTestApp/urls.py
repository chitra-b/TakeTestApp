"""TakeTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from TakeTestApp import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('register', views.RegistrationView, basename='user-register')
router.register('tests', views.PostQuestionView, basename='tests')
router.register('readytoattend', views.ReadyToAttendView, basename='readytoattend')
router.register('taketest', views.TakeTestView, basename='taketest')
router.register('answer', views.AnswersView, basename='answer')
urlpatterns = router.urls
