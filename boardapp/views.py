from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from .models import Board, Comment
from django.utils import timezone
from .forms import BoardForm, CommentForm
from django.core.paginator import Paginator
from django.contrib import messages

from mainapp.models import BoardMember
from django.views.generic import DetailView
from django.db.models import Count

#검색에 필요한 패키지 임포트
from django.views.generic.edit import FormView
from boardapp.forms import BoardSearchForm
from django.db.models import Q
from django.shortcuts import render 

# 홈(게시판 홈)
# def board(request):
#     boards = Board.objects.all().order_by('-id')
#     paginator = Paginator(boards, 5)
#     page = request.GET.get('page')
#     boards = paginator.get_page(page)
#     return render(request, 'board.html', {'boards':boards})
def board(request):
    boards = Board.objects.all().order_by('-id') #models.py Board 클래스의 모든 객체를 board_list에 담음
    # board_list 페이징 처리
    paginator = Paginator(boards, '8') #Paginator(분할될 객체, 페이지 당 담길 객체수)
    page = request.GET.get('page','1') #GET 방식으로 정보를 받아오는 데이터
    boards = paginator.get_page(page) #페이지 번호를 받아 해당 페이지를 리턴 get_page 권장
    return render(request, 'board.html', {'boards':boards}) 


# 게시글 detail 
def detail(request, id):
    board = get_object_or_404(Board, pk = id)
    return render(request, 'detail.html', {'board':board})

# 새글작성인 new.html 보여줌
def new(request):
    form = BoardForm()
    return render(request, 'new.html', {'form':form})

# def new(request):
#     if request.user.is_authenticated: 
#         #로그인 한 상태라면 new포스트 html로 보내기.
#         return render(request, 'new.html')
#     else:
#         #회원정보가 존재하지 않는다면, 에러인자와 함께 home 템플릿으로 돌아가기.     
#         boards = Board.objects.all().order_by('-id')
#         paginator = Paginator(boards, 5)
#         page = request.GET.get('page')
#         boards = paginator.get_page(page)
#         return render(request, 'board.html', {'boards': boards, 'error': 'You have to login to make newpost'})
    

# 새글을 데이터베이스에 저장
def create(request):
    form = BoardForm(request.POST, request.FILES)
    if form.is_valid():
        user_id = request.session.get('user')
        member = BoardMember.objects.get(pk=user_id)
        new_board = form.save(commit=False) #임시저장(pubdate)
        new_board.pub_date = timezone.now()
        new_board.writer = member
        new_board.save()
        return redirect('detail', new_board.id)
    return redirect('board')

# 수정기능 edit.html 보여줌
def edit(request, id):
    edit_board = Board.objects.get(id=id)
    user_id = request.session.get('user')
    member = BoardMember.objects.get(pk=user_id)
    if member != edit_board.writer:
        messages.warning(request, "수정 권한이 없습니다") 
        return redirect('detail', edit_board.id)
    
    return render(request, 'edit.html', {'board':edit_board})

# 수정 내용을 데이터베이스에 저장
def update(request, id):
    update_board = Board.objects.get(id = id)
    update_board.title = request.POST['title']
    update_board.body = request.POST['body']
    update_board.pub_date = timezone.now()
    update_board.save() # 필수!
    return redirect('detail', update_board.id)

# 삭제하기 기능
def delete(request, id):
    delete_board = Board.objects.get(id=id)

    # 글쓴이가 아닌 경우 삭제 안됨 -> 경고창 뜨도록 수정하기
    user_id = request.session.get('user')
    member = BoardMember.objects.get(pk=user_id)
    if member != delete_board.writer:
        messages.warning(request, "삭제 권한이 없습니다")
        return redirect('detail', delete_board.id)

    delete_board.delete()
    return redirect('board')

#댓글 기능
def comment(request, id): 
    board = get_object_or_404(Board, pk = id)
    form = CommentForm(request.POST)
    user_id = request.session.get('user')
    member = BoardMember.objects.get(pk=user_id)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = board
        comment.author_name = member
        comment.save()
        return redirect('detail', board.id)
    else:
        form = CommentForm()
    return render(request, "comment.html", {'form':form})


#카테고리(잡담)
def category_talk(request):
    boards = Board.objects.all().filter(category='잡담').order_by('-id')
    paginator = Paginator(boards, '8')
    page = request.GET.get('page','1')
    boards = paginator.get_page(page)
    return render(request, 'board.html', {'boards':boards})

#카테고리(후기)
def category_review(request):
    boards = Board.objects.all().filter(category='후기').order_by('-id')
    paginator = Paginator(boards, '8')
    page = request.GET.get('page','1')
    boards = paginator.get_page(page)
    return render(request, 'board.html', {'boards':boards})

#카테고리(공지)
def category_notice(request):
    boards = Board.objects.all().filter(category='공지').order_by('-id')
    paginator = Paginator(boards, '8')
    page = request.GET.get('page','1')
    boards = paginator.get_page(page)
    return render(request, 'board.html', {'boards':boards})

# 검색
class SearchFormView(FormView):
    form_class = BoardSearchForm
    template_name = 'search.html'

    def form_valid(self, form):
        searchWord = form.cleaned_data['search_word']
        post_list = Board.objects.filter(Q(title__icontains=searchWord) | Q(body__icontains=searchWord)).distinct()

        context = {}
        context['form'] = form
        context['search_term'] = searchWord
        context['object_list'] = post_list

        return render(self.request, self.template_name, context)

def mypage(request): 
    return render(request, "mypage.html")

#내가쓴글
def mypage(request):
    me = request.session.get('user')
    boards = Board.objects.all().filter(writer = me).order_by('-id')
    paginator = Paginator(boards, '8')
    page = request.GET.get('page','1')
    boards = paginator.get_page(page)
    return render(request, 'mypage.html', {'boards':boards})
    