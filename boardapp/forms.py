from django import forms #장고 제공
from .models import Board, Comment
from django import forms

# 게시글 작성폼
class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['category', 'title', 'writer', 'image', 'body']
        labels = {
            'category' : '카테고리', 
            'title' : '제목', 
            'writer' : '작성자', 
            'image' : '이미지', 
            'body' : ''
            }

# 댓글작성폼
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author_name', 'comment_text']
        labels={
            'author_name' : '작성자',
            'comment_text' : ''
        }

# 검색기능폼
class BoardSearchForm(forms.Form):
    search_word = forms.CharField(label='')

        