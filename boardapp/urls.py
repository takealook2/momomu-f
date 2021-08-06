from django.contrib import admin
from django.urls import path
from .views import * #board앱의 views.py의 모든 함수를 가져온다는 문법

urlpatterns = [
    path('', board, name="board" ),
    path('talk/', category_talk, name="talk" ),
    path('review/', category_review, name="review" ),
    path('notice/', category_notice, name="notice" ),
    path('<str:id>', detail, name="detail"),
    path('new/', new, name="new"),
    path('create/', create, name="create"),
    path('edit/<str:id>', edit, name="edit"),
    path('update/<str:id>', update, name="update"),
    path('delete/<str:id>', delete, name="delete"),
    path('comment/<str:id>', comment, name="comment"),
    path('search/', SearchFormView.as_view(), name='search'),
]