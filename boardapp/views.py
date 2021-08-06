from django.shortcuts import redirect, render, get_object_or_404
from .models import Board, Comment
from django.utils import timezone
from .forms import BoardForm, CommentForm
from django.core.paginator import Paginator

# 홈(게시판 홈)
def board(request):
    boards = Board.objects.all().order_by('-id')
    paginator = Paginator(boards, 5)
    page = request.GET.get('page')
    boards = paginator.get_page(page)
    return render(request, 'board.html', {'boards':boards})

# 게시글 detail 
def detail(request, id):
    board = get_object_or_404(Board, pk = id)
    return render(request, 'detail.html', {'board':board})

# 새글작성인 new.html 보여줌
def new(request):
    form = BoardForm()
    return render(request, 'new.html', {'form':form})

# 새글을 데이터베이스에 저장
def create(request):
    form = BoardForm(request.POST, request.FILES)
    if form.is_valid():
        new_board = form.save(commit=False) #임시저장(pubdate)
        new_board.pub_date = timezone.now()
        new_board.save()
        return redirect('detail', new_board.id)
    return redirect('board')

# 수정기능 edit.html 보여줌
def edit(request, id):
    edit_board = Board.objects.get(id=id)
    return render(request, 'edit.html', {'board':edit_board})

# 수정 내용을 데이터베이스에 저장
def update(request, id):
    update_board = Board.objects.get(id = id)
    update_board.title = request.POST['title']
    update_board.writer = request.POST['writer']
    update_board.body = request.POST['body']
    update_board.pub_date = timezone.now()
    update_board.save() # 필수!
    return redirect('detail', update_board.id)

# 삭제하기 기능
def delete(request, id):
    delete_board = Board.objects.get(id=id)
    delete_board.delete()
    return redirect('board')

#댓글 기능
def comment(request, id): 
    board = get_object_or_404(Board, pk = id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = board
        comment.save()
        return redirect('detail', board.id)
    else:
        form = CommentForm()
    return render(request, "comment.html", {'form':form})


