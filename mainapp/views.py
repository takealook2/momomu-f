from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import *

def first(request):
    return render(request, "first.html")

# 로그인 관련 함수
def home(request):
    if request.method == "GET":
        return render(request, 'home.html')

    elif request.method == "POST":
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        res_data ={}

        if not (email and password):
            res_data['error'] = '모든 값을 입력하세요!'

        else:
            member = BoardMember.objects.get(email=email)
            #print(member.id)

            if check_password(password, member.password):
                request.session['user'] = member.id
                return render(request, "first.html")

            else:
                res_data['error'] = '비밀번호가 일치하지 않습니다.'

        return render(request, 'home.html', res_data)

#로그아웃 함수
def logout(request):
    if request.session.get('user'):
        del(request.session['user'])
    return redirect('/')

#회원가입 관련 함수
def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == "POST":
        #print (request.POST)
        username    = request.POST.get('username', None)
        #print(username)
        password    = request.POST.get('password', None)
        #print(password)
        re_password = request.POST.get('re_password', None)
        #print(re_password)
        email       = request.POST.get('email', None)
        nickname    = request.POST.get('nickname', None)
        res_data = {}

        # 별명, 이메일 중복 확인(비밀번호 맞는지 아닌지 여부 확인)

        if BoardMember.objects.filter(nickname=request.POST['nickname']).exists():
            res_data['error'] = '이미 존재하는 별명입니다.'
            print(res_data)
            return render(request, 'register.html', res_data)

        if BoardMember.objects.filter(email=request.POST['email']).exists():
            res_data['error'] = '이미 존재하는 이메일입니다.'
            print(res_data)
            return render(request, 'register.html', res_data)


        if password != re_password:
            res_data['error'] = '비밀번호가 다릅니다.'
            print(res_data)
        
            return render(request, 'register.html', res_data)

        else:
            member = BoardMember(
                username    = username,
                nickname    = nickname,
                email       = email,
                password    = make_password(password)
            )
            member.save()
            return render(request, 'register_done.html', res_data)