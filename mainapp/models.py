from django.db import models

# Create your models here.

# 어드민 페이지 내에서 가입한 유저들의 정보 확인 관련 
class BoardMember(models.Model):
    username    = models.CharField(max_length=100, verbose_name='유저이름')
    nickname    = models.CharField(max_length=100, verbose_name='유저닉네임')
    email       = models.EmailField(max_length=100, verbose_name='유저이메일')
    password    = models.CharField(max_length=100, verbose_name='유저PW')
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name='가입날짜')
    updated_at  = models.DateTimeField(auto_now=True, verbose_name='마지막수정일')

    def __str__(self):
        return self.email

    class Meta:
        db_table            = 'boardmembers'
        verbose_name        = '게시판멤버'
        verbose_name_plural = '게시판멤버'