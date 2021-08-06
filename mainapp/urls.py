from django.contrib import admin
from django.urls import path
from .views import * #main앱의 views.py의 모든 함수를 가져온다는 문법

urlpatterns = [
    path('', home, name="home"),
    path('first/', first, name="first"),
    path('register/', register, name="register"),
]