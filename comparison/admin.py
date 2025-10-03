from django.contrib import admin
from .models import Image, Vote, Visitor, VisitorCounter

@admin.register(Image)
class UserImage_Admin(admin.ModelAdmin):
    list_display = ['title', 'image', 'elo_rating']

@admin.register(Vote)
class UserVote_Admin(admin.ModelAdmin):
    list_display = ['winner']

@admin.register(Visitor)    
class Visitor_Admin(admin.ModelAdmin):
    list_diaplay = ['ip_address']

@admin.register(VisitorCounter)    
class VisitorCounter_Admin(admin.ModelAdmin):
    list_diaplay = ['total_visitors']