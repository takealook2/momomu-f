from django.db import models
from django.utils import timezone

#카테고리 select 필드
category_select = (
    ('공지', '공지'),
    ('잡담', '잡담'),
    ('후기', '후기')
)

class Board(models.Model):
    category = models.CharField(max_length=20, choices=category_select, default='잡담')
    title = models.CharField(max_length=200)
    writer = models.CharField(max_length=100)
    pub_date = models.DateTimeField()
    body = models.TextField()
    image = models.ImageField(upload_to = "board/", blank=True, null=True)
    #->오류나면 "board/"이부분 수정해보기 ->boardapp/으로??
    board_hit = models.PositiveIntegerField(default=0)
    #->조회수 기능

    def __str__(self):
        return self.title #제목으로 보이게
    
    def summary(self):
        return self.body[:100]

    #조회수 counter (문제: f5누르면 쭈~욱 올라감)
    @property
    def update_counter(self):
        self.board_hit = self.board_hit + 1
        self.save()

#댓글 관련 모델
class Comment(models.Model):
    post = models.ForeignKey(Board, related_name='comments', on_delete=models.CASCADE)
    author_name=models.CharField(max_length=20) 
    comment_text=models.TextField() 
    created_at=models.DateTimeField(default=timezone.now) #장고에서 기본으로 제공됨 
    # 들어갈 내용들 : 댓글 작성자, 댓글 내용, 댓글 작성 시간

    def approve(self):
        self.save()

    def __str__(self): 
        return self.comment_text