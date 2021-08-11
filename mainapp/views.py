from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from mainapp import models
from selenium import webdriver
from bs4 import BeautifulSoup

def first(request):
    return render(request, "first.html")

def about(request): 
    return render(request, "about.html")

def mbti(request): 
    return render(request, "mbti.html")

def index(request): 
    return render(request, "index.html")

def mi(request): 
    return render(request, "mi.html")

def rank(request): 
    return render(request, "rank.html")

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
                request.session['username'] = member.username
                request.session['nickname'] = member.nickname
                request.session['email'] = member.email
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

def musical(request):
    webdriver_options = webdriver.ChromeOptions()
    webdriver_options .add_argument('headless')

    chromedriver = './chromedriver.exe'
    brower = webdriver.Chrome(chromedriver, options=webdriver_options )

    # brower = webdriver.Chrome('./chromedriver.exe')

    url = "http://ticket.interpark.com/contents/Ranking/RankList?pKind=01011&pCate=01011&pType=M&pDate="
    brower.get(url)

    html = brower.page_source
    soup = BeautifulSoup(html, 'html.parser')

    #뮤지컬 월간 top10 제목
    title1 = soup.select('div.prdInfo')[0]['title']
    title2 = soup.select('div.prdInfo')[1]['title']
    title3 = soup.select('div.prdInfo')[2]['title']
    title4 = soup.select('div.prdInfo')[3]['title']
    title5 = soup.select('div.prdInfo')[4]['title']
    title6 = soup.select('div.prdInfo')[5]['title']
    title7 = soup.select('div.prdInfo')[6]['title']
    title8 = soup.select('div.prdInfo')[7]['title']
    title9 = soup.select('div.prdInfo')[8]['title']
    title10 = soup.select('div.prdInfo')[9]['title']

    #뮤지컬 월간 top10 장소
    place1_1 = soup.select('div.prdInfo > a')[0].text
    place1_1 = place1_1.strip()
    place1_2 = soup.select('div.prdInfo > a > b')[0].text
    place1_2 = place1_2.strip()
    place1_3 = place1_1[len(place1_2)+1:]
    place1 = place1_3.strip()

    place2_1 = soup.select('div.prdInfo > a')[1].text
    place2_1 = place2_1.strip()
    place2_2 = soup.select('div.prdInfo > a > b')[1].text
    place2_2 = place2_2.strip()
    place2_3 = place2_1[len(place2_2)+1:]
    place2 = place2_3.strip()

    place3_1 = soup.select('div.prdInfo > a')[2].text
    place3_1 = place3_1.strip()
    place3_2 = soup.select('div.prdInfo > a > b')[2].text
    place3_2 = place3_2.strip()
    place3_3 = place3_1[len(place3_2)+1:]
    place3 = place3_3.strip()

    place4_1 = soup.select('div.prdInfo > a')[3].text
    place4_1 = place4_1.strip()
    place4_2 = soup.select('div.prdInfo > a > b')[3].text
    place4_2 = place4_2.strip()
    place4_3 = place4_1[len(place4_2)+1:]
    place4 = place4_3.strip()

    place5_1 = soup.select('div.prdInfo > a')[4].text
    place5_1 = place5_1.strip()
    place5_2 = soup.select('div.prdInfo > a > b')[4].text
    place5_2 = place5_2.strip()
    place5_3 = place5_1[len(place5_2)+1:]
    place5 = place5_3.strip()

    place6_1 = soup.select('div.prdInfo > a')[5].text
    place6_1 = place6_1.strip()
    place6_2 = soup.select('div.prdInfo > a > b')[5].text
    place6_2 = place6_2.strip()
    place6_3 = place6_1[len(place6_2)+1:]
    place6 = place6_3.strip()

    place7_1 = soup.select('div.prdInfo > a')[6].text
    place7_1 = place7_1.strip()
    place7_2 = soup.select('div.prdInfo > a > b')[6].text
    place7_2 = place7_2.strip()
    place7_3 = place7_1[len(place7_2)+1:]
    place7 = place7_3.strip()

    place8_1 = soup.select('div.prdInfo > a')[7].text
    place8_1 = place8_1.strip()
    place8_2 = soup.select('div.prdInfo > a > b')[7].text
    place8_2 = place8_2.strip()
    place8_3 = place8_1[len(place8_2)+1:]
    place8 = place8_3.strip()

    place9_1 = soup.select('div.prdInfo > a')[8].text
    place9_1 = place9_1.strip()
    place9_2 = soup.select('div.prdInfo > a > b')[8].text
    place9_2 = place9_2.strip()
    place9_3 = place9_1[len(place9_2)+1:]
    place9 = place9_3.strip()

    place10_1 = soup.select('div.prdInfo > a')[9].text
    place10_1 = place10_1.strip()
    place10_2 = soup.select('div.prdInfo > a > b')[9].text
    place10_2 = place10_2.strip()
    place10_3 = place10_1[len(place10_2)+1:]
    place10 = place10_3.strip()

    #뮤지컬 월간 top10 날짜
    date1 = soup.select('td.prdDuration')[0].text
    date2 = soup.select('td.prdDuration')[1].text
    date3 = soup.select('td.prdDuration')[2].text
    date4 = soup.select('td.prdDuration')[3].text
    date5 = soup.select('td.prdDuration')[4].text
    date6 = soup.select('td.prdDuration')[5].text
    date7 = soup.select('td.prdDuration')[6].text
    date8 = soup.select('td.prdDuration')[7].text
    date9 = soup.select('td.prdDuration')[8].text
    date10 = soup.select('td.prdDuration')[9].text

    #뮤지컬 월간 top10 이미지
    img1 = soup.select('td.prds > a > img')[0]['src']
    img2 = soup.select('td.prds > a > img')[1]['src']
    img3 = soup.select('td.prds > a > img')[2]['src']
    img4 = soup.select('td.prds > a > img')[3]['src']
    img5 = soup.select('td.prds > a > img')[4]['src']
    img6 = soup.select('td.prds > a > img')[5]['src']
    img7 = soup.select('td.prds > a > img')[6]['src']
    img8 = soup.select('td.prds > a > img')[7]['src']
    img9 = soup.select('td.prds > a > img')[8]['src']
    img10 = soup.select('td.prds > a > img')[9]['src']

    return render(request, 'rank.html', {'title1':title1, 'title2':title2, 'title3':title3,'title4':title4, 'title5':title5, 'title6':title6, 'title7':title7, 'title8':title8, 'title9':title9, 'title10':title10,
    'place1':place1, 'place2':place2, 'place3':place3, 'place4':place4, 'place5':place5, 'place6':place6, 'place7':place7, 'place8':place8, 'place9':place9, 'place10':place10,
    'date1':date1, 'date2':date2, 'date3':date3, 'date4':date4, 'date5':date5, 'date6':date6, 'date7':date7, 'date8':date8, 'date9':date9, 'date10':date10,
    'img1':img1, 'img2':img2, 'img3':img3, 'img4':img4, 'img5':img5, 'img6':img6, 'img7':img7, 'img8':img8, 'img9':img9, 'img10':img10})

    