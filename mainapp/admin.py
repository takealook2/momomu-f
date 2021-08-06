from django.contrib import admin
from .models import *

class BoardMemberAdmin(admin.ModelAdmin):
    list_display = ('username', 'nickname','email', 'password', 'created_at', 'updated_at')

admin.site.register(BoardMember, BoardMemberAdmin)
