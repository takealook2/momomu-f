from django import forms #장고 제공
from .models import Board, Comment

# 게시글 작성폼
class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'writer', 'image', 'body']

# 댓글작성폼
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author_name', 'comment_text']

        