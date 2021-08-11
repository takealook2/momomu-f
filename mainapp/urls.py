from boardapp.views import mypage
from os import name
from django.contrib import admin
from django.urls import path
from .views import * #main앱의 views.py의 모든 함수를 가져온다는 문법
from mainapp import views

urlpatterns = [
    path('', home, name="home"),
    path('first', first, name="first"),
    path('first/', views.img, name="img"),
    path('register/', register, name="register"),
    path('about', about, name="about"),
    path('mbti', mbti, name="mbti"),
    path('index', index, name="index"),
    path('logout/', logout, name="logout"),
    path('mi', mi, name="mi"),
    path('rank', rank, name="rank"),
    path('rank/', views.musical, name="musical"),
    path('mypage', mypage, name="mypage")
]